class Project:
    projects: dict[str, 'Project'] = {}  # Type hint for class attribute

    def __init__(self, name: str, resource_name: str, description: str) -> None:
        self.name: str = name
        self.resource_name: str = resource_name
        self.description: str = description
    
    @classmethod
    def create(cls, name: str, resource_name: str, description: str) -> 'Project':
        if name in cls.projects:
            raise ValueError("Project with this name already exists.")
        cls.projects[name] = Project(name, resource_name, description)
        return cls.projects[name]

    @classmethod
    def read(cls, name: str) -> 'Project' or None:
        return cls.projects.get(name, None)

    @classmethod
    def update(cls, name: str, **kwargs) -> 'Project' or None:
        project = cls.projects.get(name)
        if not project:
            return None
        
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        return project

    @classmethod
    def delete(cls, name: str) -> str:
        if name in cls.projects:
            del cls.projects[name]
            return f"Project '{name}' deleted."
        return "Project not found."
