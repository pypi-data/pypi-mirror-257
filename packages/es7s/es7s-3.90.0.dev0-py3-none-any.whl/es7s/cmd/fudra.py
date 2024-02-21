# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import base64
import io
import json
import os
import re
import sys
import time
import typing as t
from collections import deque, Counter
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import cached_property
from math import floor
from threading import Lock
from uuid import UUID

import psutil
import pytermor as pt
from PIL import Image, ImageFont
from PIL.ImageDraw import Draw

from es7s.cmd._base import _BaseAction
from es7s.shared import (
    get_logger,
    get_stdout,
    ShutdownableThread,
    with_terminal_state,
    ProxiedTerminalState,
    ShutdownInProgress, boolsplit, )
from es7s.shared.fusion_brain import FusionBrainAPI
from es7s.shared.path import get_font_file
from es7s.shared.uconfig import get_merged, get_for


class action(_BaseAction):
    def __init__(
        self,
        threads: int,
        prompt: list[str],
        stdin: bool,
        style: str,
        **kwargs,
    ):
        self._threads = threads
        if threads < 1:
            # threads_limit = self.uconfig().get("auto-threads-limit", int)
            self._threads = max(1, psutil.cpu_count())
        if stdin:
            prompt = sys.stdin.readlines()
        if not prompt:
            get_stdout().echo("Empty input")
            return

        auth_cfg = get_merged().get_section("auth")
        self._api = FusionBrainAPI(
            auth_cfg.get("fusion-brain-api-key"),
            auth_cfg.get("fusion-brain-secret"),
        )
        self._api.fetch_model()
        style_names = self._api.fetch_styles()
        get_logger().info("Supported styles: " + ", ".join(style_names))
        if style not in style_names:
            # style_fb = style_names[-1]
            get_logger().warning(f"Unsupported style '{style}'") #, falling back to '{style_fb}'")
            # style = style_fb

        self._queue = Queue(self._api, self._threads, prompt, style, **kwargs)
        self._run()

    @with_terminal_state(no_cursor=True)
    def _run(self, termstate: ProxiedTerminalState):
        try:
            self._queue.run()
        finally:
            self._queue.destroy()


class Queue:
    _THREAD_POLL_TIME_SEC = 0.1

    start_ts: float = None

    @staticmethod
    def now() -> float:
        return time.time_ns()

    def __init__(
        self,
        api: FusionBrainAPI,
        threads: int,
        prompt_raw: list[str],
        style: str,
        times: int,
        no_retry: bool,
        keep: bool,
        **kwargs,
    ):
        self.tasks = deque[Task]()
        self.tasks_done = deque[Task]()
        self.tasks_lock = Lock()
        self.style = style
        self.keep_origins = keep
        self._workers = deque[Worker](maxlen=threads)
        self._exceptions = deque[tuple['Worker', t.Optional['Task'], Exception]]()
        self.pp = ProgressPrinter()
        super().__init__()

        prompt_resplitted = [*pt.filterf(pt.flatten([p.splitlines() for p in prompt_raw]))]
        tasks_total = times * len(prompt_resplitted)
        for r_idx in range(times):
            for (p_idx, p) in enumerate(prompt_resplitted):
                task_idx = len(self.tasks)
                pre_start_delay_s = task_idx/2 if task_idx < threads else 0
                task = Task(p, p_idx, task_idx, tasks_total, pre_start_delay_s)
                self.tasks.append(task)

        for w_idx in range(min(len(self.tasks), threads)):
            self._workers.append(Worker(w_idx, no_retry, self, api.copy()))

    def run(self):
        Queue.start_ts = Queue.now()

        for worker in self._workers:
            worker.start()

        while self._workers:
            worker: Worker = self._workers[0]
            worker.join(self._THREAD_POLL_TIME_SEC)

            if worker.is_alive():
                # self.pp.update(worker.task)  # avoid complete freezing on network delays
                self._workers.rotate()
            else:
                self._workers.remove(worker)

    def get_next_task(self) -> t.Optional["Task"]:
        if not self.tasks:
            return None
        if self.tasks_lock.acquire(timeout=1):
            task = self.tasks.popleft()
            task.task_start_ts = self.now() + task.pre_start_delay_s * 1e9
            self.tasks_lock.release()
            return task
        return None

    def set_task_completed(self, task: "Task"):
        task.is_finished = True
        self.tasks_done.append(task)

    def defer_exception(self, worker: 'Worker', task: t.Optional['Task'], e: Exception):
        self._exceptions.append((worker, task, e))

    def destroy(self):
        self.pp.close()

        for e in self._exceptions:
            self.pp.print_exception(*e)

        results = []
        for task in self.tasks_done:
            results.extend(task.statuses)
        results_by_type = Counter(results)
        avg_job_durations_ns = [*pt.filtern(t.avg_job_duration for t in self.tasks_done)]
        avg_job_duration_s = 0
        if avg_job_durations_ns:
            avg_job_duration_s = (sum(avg_job_durations_ns) / len(avg_job_durations_ns)) / 1e9
        self.pp.print_summary(results_by_type, avg_job_duration_s)


class Status(str, pt.ExtendedEnum):
    QUEUED = "queued"

    PENDING = "pending"
    REFUSED = "refused"
    RECEIVED = "received"
    ERROR = "error"

    CANCEL = "cancel"
    FAILURE = "failure"
    SUCCESS = "success"


@dataclass(frozen=True)
class StatusStyle:
    char: pt.RT = " "
    name: pt.FT = pt.NOOP_STYLE
    duration: pt.FT = pt.cv.BLUE

    @cached_property
    def msg(self) -> pt.FT:
        if self.name:
            return pt.FrozenStyle(self.name, bold=True)
        return pt.NOOP_STYLE


STATUS_STYLES = {
    Status.QUEUED: StatusStyle("⋅", pt.make_style("gray_50"), pt.make_style("gray_50")),
    Status.PENDING: StatusStyle("▯"),
    Status.REFUSED: StatusStyle(pt.Fragment("▮", "yellow"), pt.make_style("yellow")),
    Status.RECEIVED: StatusStyle(pt.Fragment("▯", "green"), pt.make_style("green")),
    Status.ERROR: StatusStyle(pt.Fragment("▯", "red"), pt.make_style("red")),
    Status.CANCEL: StatusStyle(pt.Fragment("▯", "red"), pt.make_style("red")),
    Status.FAILURE: StatusStyle(pt.Fragment("▮", "red"), pt.make_style("red")),
    Status.SUCCESS: StatusStyle(pt.Fragment("▮", "green"), pt.make_style("green")),
}


@dataclass()
class Task:
    MIN_FETCH_INTERVAL_SEC = 4

    prompt: str
    prompt_idx: int
    task_idx: int
    tasks_total: int
    pre_start_delay_s: float = 0.0

    max_width: int = pt.get_terminal_width()

    job_uuid: UUID | None = None
    images: list[str] = field(default_factory=list)
    statuses: list[Status] = field(default_factory=list)
    task_start_ts: float | None = None
    job_start_ts: float | None = None
    last_fetch_ts: float | None = None
    task_duration_ns: float | None = None
    job_durations_ns: list[float] = field(default_factory=list)
    jobs_done: int = 0
    msg: str | tuple[str, str] | None = None
    is_finished: bool = False

    @property
    def current_status(self) -> Status:
        if not self.statuses:
            return Status.QUEUED
        return self.statuses[-1]

    @property
    def avg_job_duration(self) -> float | None:
        if self.jobs_done:
            return sum(self.job_durations_ns) / self.jobs_done
        return None

    def assign_job_uuid(self, uuid: UUID):
        self.job_uuid = uuid
        self.job_start_ts = Queue.now()
        self.last_fetch_ts = None

    def is_allowed_to_generate(self) -> bool:
        return Queue.now() >= self.task_start_ts

    def is_allowed_to_fetch(self) -> bool:
        if self.last_fetch_ts is None:
            return True
        return (Queue.now() - self.last_fetch_ts) / 1e9 >= self.MIN_FETCH_INTERVAL_SEC

    def set_status(self, rr: Status, msg: str | tuple[str, str] = None):
        self.statuses.append(rr)
        self.msg = msg
        self.last_fetch_ts = Queue.now()
        self.task_duration_ns = Queue.now() - self.task_start_ts

    def append_images(self, images: list[str]):
        self.images += images
        self.set_status(Status.RECEIVED)
        self.job_durations_ns.append(Queue.now() - self.job_start_ts)
        self.job_start_ts = None
        self.jobs_done += 1

    def print_state(self) -> pt.RT:
        sts = STATUS_STYLES.get(self.current_status)
        st0 = pt.NOOP_STYLE
        stm = lambda c: st0.clone().merge_overwrite(pt.make_style(c))
        stmf = lambda c: st0.clone().merge_fallback(pt.make_style(c))
        if self.is_finished:
            st0 = stm(pt.Style(fg=pt.cv.GRAY_50))

        cols = []
        cols.append(pt.Fragment(f"{self.task_idx + 1:>2d}/{self.tasks_total:<2d}", st0))
        cols.append(pt.pad(1))
        cols.append(pt.Fragment(pt.fit("'" + pt.cut(self.prompt, 12, "<") + "'", 14), st0))
        cols.append(pt.pad(1))

        if not self.msg:
            cols.append(pt.Fragment(pt.fit(str(self.job_uuid or ""), 30), st0))
        else:
            cols.append(pt.Fragment(self._print_msg(self.msg, 30, 1), stm(sts.msg)))
        cols.append(pt.pad(1))

        if self.task_start_ts:
            col_dur = pt.format_time_delta((Queue.now() - self.task_start_ts) / 1e9).rjust(8)
        else:
            col_dur = pt.fit("---", 8, ">")
        cols.append(pt.Fragment(col_dur, stmf(sts.duration)))
        cols.append(pt.pad(1))

        cols.append(pt.Fragment(self.current_status.value.rjust(9), stm(sts.name)))
        cols.append(pt.pad(1))

        cols.extend(self._print_status_history(st0))
        return pt.Text(*cols, width=ProgressPrinter.get_max_width())

    def _print_msg(self, msg: str | tuple[str, str], maxlen: int = 30, gap: int = 2) -> str:
        if isinstance(msg, tuple):
            return pt.fit(msg[0], maxlen - len(msg[1]) - gap, "<") + pt.pad(gap) + msg[1]
        return pt.fit(self.msg, maxlen, "<", keep="<")

    def _print_status_history(self, base_st: pt.Style) -> Iterable[pt.Fragment]:
        for status in self.statuses:
            char = STATUS_STYLES.get(status).char
            if isinstance(char, str):
                yield pt.Fragment(char, base_st)
            else:
                yield char


class Worker(ShutdownableThread):
    _POLL_TIME_SEC = 0.15

    LABEL_FONT = ImageFont.truetype(str(get_font_file('Smallest_Pixel_7_Regular.ttf')), 10)

    def __init__(
        self,
        worker_idx: int,
        no_retry: bool,
        queue: Queue,
        api: FusionBrainAPI,
    ):
        self.worker_idx = worker_idx
        self._no_retry = no_retry
        self._queue = queue
        self._api = api

        self.task: Task | None = None

        super().__init__("fudra", thread_name=f"worker:{self.worker_idx}")

    def _reset(self):
        self.task = None

    def run(self):
        while True:
            if self.is_shutting_down():
                self.destroy()
                return

            if not self.task:
                self.task = self._queue.get_next_task()
                if not self.task:
                    self.shutdown()
                    continue

            if self.task:
                try:
                    self._generate()
                    self._write_image()
                except ShutdownInProgress:
                    pass
                except Exception as e:
                    self._queue.defer_exception(self, self.task, e)
                    self.task.set_status(Status.FAILURE, repr(e))
                finally:
                    self._queue.set_task_completed(self.task)
                    self._redraw()
                    self._reset()

    def _update(self):
        self._queue.pp.update(self.task)

    def _redraw(self):
        self._queue.pp.redraw(self.task)

    def _tick(self):
        if self.is_shutting_down():
            self.task.set_status(Status.CANCEL)
            raise ShutdownInProgress
        time.sleep(self._POLL_TIME_SEC)
        self._update()

    def _generate(self):
        gen_attempts = 1 if self._no_retry else 5
        while gen_attempts > 0 and len(self.task.images) == 0:
            if not self.task.is_allowed_to_generate():
                self._tick()
                continue

            gen_attempts -= 1
            negprompt, posprompt = boolsplit(self.task.prompt.split(), lambda p: bool(re.match(r'^-[^-]', p)))
            negprompt = [np.removeprefix('-') for np in negprompt]
            generation_uuid = self._api.generate(' '.join(posprompt), negprompt=negprompt, style=self._queue.style)
            self.task.assign_job_uuid(generation_uuid)
            self._update()

            fetch_attempts = 30
            while fetch_attempts > 0:
                self._tick()

                if self.task.is_allowed_to_fetch():
                    fetch_attempts -= 1
                    images, censored, resp = self._api.check_generation(self.task.job_uuid)

                    if not resp.ok:
                        self.task.set_status(Status.ERROR, f"HTTP {resp.status_code}")
                    elif censored:
                        self.task.set_status(Status.REFUSED, str(self.task.job_uuid))
                    elif len(images) > 0:
                        self.task.append_images(images)
                    else:
                        self.task.set_status(Status.PENDING)

                    self._update()
                    if self.task.current_status != Status.PENDING:
                        break

            self._update()

    def _write_image(self):
        if not self.task.images:
            return

        output_dir = os.path.expanduser(get_for(self).get("output-dir", str, fallback="~"))
        os.makedirs(output_dir, exist_ok=True)

        basename = f"fb-{Queue.start_ts / 1e9:.0f}-{self.task.prompt_idx}-{self.task.task_idx}"
        with open(os.path.join(output_dir, f"{basename}.json"), "wt") as f:
            json.dump(dict(prompt=self.task.prompt), f)

        for idx, img_b64 in enumerate(self.task.images):
            img_in = io.BytesIO(img_b64.encode("utf8"))
            img_out = io.BytesIO()
            base64.decode(img_in, img_out)
            del img_in

            suffix = f"-{idx}" if idx > 0 else ""
            last_img_path = os.path.join(output_dir, f"{basename}{suffix}%s.jpg")

            keep_origins = self._queue.keep_origins
            try:
                self._write_image_label(img_out, last_img_path % "")
            except Exception as e:
                self._queue.defer_exception(self, self.task, e)
                keep_origins = True

            if keep_origins:
                self._write_image_origin(img_out, last_img_path % "-origin")
            del img_out

    def _write_image_origin(self, img_out: io.BytesIO, img_path: str):
        img_out.seek(0)
        with open(img_path, "wb") as f:
            f.write(img_out.read())

    def _write_image_label(self, img_out: io.BytesIO, img_path: str):
        prompt = self.task.prompt
        prompt_split = []

        im = Image.open(img_out).convert('RGBA')
        while prompt:
            tlen = Draw(im).textlength(prompt, self.LABEL_FONT)
            overflow_ratio = tlen / (im.width / 2)
            edge = len(prompt) / overflow_ratio
            if edge <= 1:
                prompt_split.append(prompt)
                prompt = ""
            else:
                edge = floor(edge)
                prompt_split.append(prompt[:edge])
                prompt = prompt[edge:]

        imtx = Image.new("RGBA", im.size, (255, 255, 255, 0))
        Draw(imtx).multiline_text(
            (0, 0),
            fill=(255, 255, 255, 128),
            stroke_fill=(0, 0, 0, 128),
            stroke_width=1,
            text="\n".join(prompt_split),
            font=self.LABEL_FONT,
            spacing=0,
        )
        im.paste(imtx, None, imtx)
        del imtx

        with open(img_path, "wb") as f:
            im.convert("RGB").save(f)

        last_img_info = (
            os.path.basename(img_path),
            pt.format_bytes_human(os.stat(img_path).st_size).rjust(5),
        )
        self.task.set_status(Status.SUCCESS, last_img_info)


class ProgressPrinter:
    _ts_last_termw_query: float = None
    _max_width: int = None

    def __init__(self):
        self._redraw_lock = Lock()
        self._cursor_line = 0
        self._task_lines: deque[Task | None] = deque()

    def update(self, task: Task):
        if not task:
            return
        with self._redraw_lock:
            if task not in self._task_lines:
                self._go_to_bottom()
                self._task_lines.append(task)
            else:
                task_line = self._task_lines.index(task)
                self._go_to(task_line)
            self._draw(task)

    def redraw(self, task: Task):
        self.update(task)
        with self._redraw_lock:
            self._task_lines[self._task_lines.index(task)] = None

    def _draw(self, task: Task, suffix: str = ""):
        get_stdout().echoi_rendered('\n'+task.print_state() + suffix)
        get_stdout().echoi(pt.make_move_cursor_up())

    def _go_to(self, target_line: int):
        delta = abs(self._cursor_line - target_line)
        if self._cursor_line > target_line:
            get_stdout().echoi(pt.make_move_cursor_up(delta))
        elif self._cursor_line < target_line:
            get_stdout().echoi(pt.make_move_cursor_down(delta))
        get_stdout().echoi(pt.make_set_cursor_column())
        self._cursor_line = target_line

    def _go_to_bottom(self):
        self._go_to(len(self._task_lines))

    def _clear_line(self):
        get_stdout().echoi(pt.make_clear_line())

    def close(self):
        self._go_to_bottom()
        get_stdout().echo("")

    def print_exception(self, worker: Worker, task: Task|None, e: Exception):
        get_stdout().echo_rendered(pt.Text(
            pt.Fragment(f"Worker #{worker.worker_idx+1}", pt.Styles.ERROR),
            pt.pad(2),
            pt.Fragment(f"Task #{task.task_idx+1}", pt.Styles.ERROR_LABEL),
            pt.pad(2),
            pt.Fragment(repr(e), pt.Styles.ERROR)
        ))

    def print_summary(self, results_by_type: Counter[Status], avg_job_duration_s: float):
        refused = results_by_type.get(Status.REFUSED) or 0
        recevied = results_by_type.get(Status.RECEIVED) or 0
        requested = refused + recevied
        if requested > 0:
            refusal_ratio = 100 * refused / requested
        else:
            refusal_ratio = 0

        st_refcnt = pt.Style(fg=pt.cv.YELLOW)
        if refused == 0:
            st_refcnt.fg = pt.cv.GRAY_50
        st_refrat = pt.Style(st_refcnt, bold=True)

        get_stdout().echo("")
        print_summary_line = lambda t, *f: get_stdout().echo_rendered(
            pt.Text(pt.fit(t, 14, '>') + ':', pt.pad(1), *f)
        )
        print_summary_line(
            "Refusal rate",
            (f"{refusal_ratio:3.1f}%", st_refrat),
            f" ({pt.Fragment(str(refused), st_refcnt)}/{requested})",
        )
        print_summary_line(
            "Avg. job time",
            pt.format_time_delta(avg_job_duration_s),
        )

    @classmethod
    def get_max_width(cls) -> int:
        if not cls._max_width or (time.time() - cls._ts_last_termw_query >= 1):
            cls._max_width = pt.get_terminal_width()
            cls._ts_last_termw_query = time.time()
        return cls._max_width
