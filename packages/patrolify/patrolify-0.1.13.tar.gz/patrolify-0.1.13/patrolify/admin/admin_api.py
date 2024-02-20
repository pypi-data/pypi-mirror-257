import json
import logging
from pathlib import Path
from flask import Blueprint, Response, jsonify, request
from patrolify.globals import g
from patrolify.consts import RESULT_FILE_NAME
from patrolify.queue_jobs import trigger_target
from patrolify.reports import (
    get_check_report,
    get_latest_check_ids,
    get_result_by_job_id,
)
from rq import Worker


logger = logging.getLogger(__name__)
admin_api_blueprint = Blueprint("admin_api", __name__, url_prefix="/api/v1")


@admin_api_blueprint.route("/triggers")
def triggers_list():
    checker_queue = g.checker_queue
    scheduled_jobs = checker_queue.scheduled_job_registry

    list_of_job_instances = g.scheduler.get_jobs()

    scheduled_triggers = list(
        {"name": j.args[0], "description": j.args[1]} for j in list_of_job_instances
    )

    checkers = []
    for trigger in scheduled_triggers:
        report_path = get_latest_report_dir(trigger["name"])
        if not report_path:
            checkers.append({
                "name": trigger["name"],
                "description": trigger["description"],
                "latest_report_dir": None,
                "latest_report_timestamp": None,
                "report": None,
            })
            continue
        checkers.append({
            "name": trigger["name"],
            "description": trigger["description"],
            "latest_report_dir": str(report_path),
            "latest_report_timestamp": str(report_path.name),
            "report": get_report_by_path(report_path),
        })

    return jsonify({
        "scheduled_jobs_count": scheduled_jobs.count,
        "checkers": checkers,
    })


@admin_api_blueprint.route("/checker/<name>")
def checker_detail(name):
    latest_check_ids = [str(x).strip() for x in get_latest_check_ids(name)]

    result = {}
    for check_id in latest_check_ids:
        result[check_id] = get_check_report(name, check_id)

    return jsonify(result)


@admin_api_blueprint.route("/checker/<name>/latest-result")
def checker_latest_result(name):
    latest_check_ids = get_latest_check_ids(name)
    latest_one = latest_check_ids[-1].strip()
    result = get_check_report(name, latest_one)
    return jsonify(result)


@admin_api_blueprint.route("/checker/<name>/<int:check_id>")
def result_by_check_id(name, check_id):
    return jsonify(get_check_report(name, str(check_id)))


@admin_api_blueprint.route("/checker/<name>/<int:check_id>/<job_id>")
def result_by_job_id(name, check_id, job_id):
    return jsonify(get_result_by_job_id(name, str(check_id), job_id))


@admin_api_blueprint.route("/checker/<name>/enqueue", methods=["POST"])
def enqueue_checker(name):
    result = g.checker_queue.enqueue(trigger_target, name, True)
    logger.info("enqueue a job now, result: %s", result)
    return jsonify({})


@admin_api_blueprint.route("/file")
def get_file():
    path = request.args.get("path")
    logger.info("Get file path=%s", path)
    if not path:
        return Response("path in query params is requied", status=400)

    if path.startswith("checkers"):
        target = Path(g.checker_path) / path.removeprefix("checkers").removeprefix("/")
    elif path.startswith("results"):
        target = Path(g.result_path) / path.removeprefix("results").removeprefix("/")
    else:
        return Response(
            f"path {path} is not allowed, only checkers path checkers and"
            " result path results is allowed",
            status=403,
        )

    if not target.exists():
        return Response(f"{target} do not exist. {g.checker_path}", status=404)

    if target.is_dir():
        return jsonify({
            "type": "directory",
            "files": [{"name": x.name, "is_dir": x.is_dir()} for x in target.iterdir()],
        })
    if target.is_file():
        with open(target) as f:
            return jsonify({"type": "file", "content": f.read()})

    return Response("unsupported type", status=400)


@admin_api_blueprint.route("/monitor-info")
def monitor_info():
    workers = Worker.all(connection=g.redis)

    workers_data = [
        {
            "hostname": worker.hostname,
            "pid": worker.pid,
            "queues": worker.queue_names(),
            "state": worker.state,
            "last_heartbeat": worker.last_heartbeat,
            "birth_date": worker.birth_date,
            "successful_job_count": worker.successful_job_count,
            "failed_job_count": worker.failed_job_count,
            "total_working_time": worker.total_working_time,
        }
        for worker in workers
    ]

    info = g.redis.info()

    return jsonify({
        "total_worker_count": len(workers),
        "workers": workers_data,
        "checker_queue": {
            "count": g.checker_queue.count,
            "started_job": g.checker_queue.started_job_registry.count,
            "finished_job": g.checker_queue.finished_job_registry.count,
            "failed_job": g.checker_queue.failed_job_registry.count,
        },
        "reporter_queue": {
            "count": g.reporter_queue.count,
            "started_job": g.reporter_queue.started_job_registry.count,
            "finished_job": g.reporter_queue.finished_job_registry.count,
            "failed_job": g.reporter_queue.failed_job_registry.count,
        },
        "redis": {"used_memory_human": info["used_memory_human"]},
    })


def get_latest_report_dir(trigger_name):
    report_dir = g.report_base_dir(trigger_name)

    if not report_dir.exists():
        return None
    report_dirs = sorted(report_dir.iterdir())
    logger.info("year list: %s", report_dirs)

    report_dir = report_dirs[-1]
    report_dirs = sorted(report_dir.iterdir())
    logger.info("month list: %s", report_dirs)

    report_dir = report_dirs[-1]
    report_dirs = sorted(report_dir.iterdir())
    logger.info("day list: %s", report_dirs)

    report_dir = report_dirs[-1]
    report_dirs = sorted(report_dir.iterdir())
    logger.info("hour list: %s", report_dirs)

    report_dir = report_dirs[-1]
    report_dirs = sorted(report_dir.iterdir())
    logger.info("ts list: %s", report_dirs)

    report_dir = report_dirs[-1]
    logger.info("latest report dir is: %s", report_dir)

    return report_dir


def get_report_by_path(path):
    with open(path / RESULT_FILE_NAME) as f:
        return json.load(f)
