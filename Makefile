run:
	bash -c "source .venv/bin/activate && uvicorn simple_backend.src.task_tracker.main:app --reload"

venv:
	bash -c "source .venv/bin/activate"