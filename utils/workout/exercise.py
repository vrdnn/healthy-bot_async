from utils.db_api.database import WorkoutIteration


async def get_next_and_prev_iteration_id(current_iteration: WorkoutIteration):
    iteration_ids = [iteration_id[0] for iteration_id in
                     await WorkoutIteration.filter(
                         WorkoutIteration.workout_id == current_iteration.workout_id, select_values=['id']
                     )]
    prev_iterations = [iteration_id for iteration_id in iteration_ids if iteration_id < current_iteration.id]
    prev_iteration_id = prev_iterations[-1] if prev_iterations else None

    next_iterations = [iteration_id for iteration_id in iteration_ids if iteration_id > current_iteration.id]
    next_iteration_id = next_iterations[0] if next_iterations else None

    return prev_iteration_id, next_iteration_id
