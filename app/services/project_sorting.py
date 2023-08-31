async def get_projects_by_completion_rate(projects: list) -> list:
    sorted_projects = sorted(
        projects,
        key=lambda project: project.close_date - project.create_date
    )
    formatted_projects = [
        {
            "name": project.name,
            "duration": str(project.close_date - project.create_date),
            "description": project.description
        }
        for project in sorted_projects
    ]
    return formatted_projects
