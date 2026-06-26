from fastapi import APIRouter

from app.services.scheduler_service import scheduler


router = APIRouter(
    prefix="/debug",
    tags=["Debug"]
)


@router.get("/jobs")
def get_jobs():

    jobs = []

    for job in scheduler.get_jobs():

        jobs.append(
            {
                "id": job.id,
                "next_run": str(
                    job.next_run_time
                )
            }
        )

    return jobs