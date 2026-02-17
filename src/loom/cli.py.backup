import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional, List
import json

from .core import OSSProject, Relationship, RelationshipType, CapabilityType, Intent
from .graph import SemanticGraph
from .weaver import PatternWeaver

console = Console()

# Create the main app
app = typer.Typer(
    help="LOOM: The Open-Source Pattern Weaver",
    invoke_without_command=True,
    no_args_is_help=True,
)

# Initialize the semantic graph (shared instance)
_graph_instance = None

def get_graph():
    """Get or create the shared graph instance."""
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = SemanticGraph()
    return _graph_instance

@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", help="Show version"
    )
):
    """Loom - Weave OSS capabilities into emergent architectures."""
    if version:
        console.print("Loom v0.1.0")
        raise typer.Exit()

@app.command()
def hello():
    """Simple test command to verify Loom is working."""
    console.print(Panel.fit(
        "[bold green]🧵 Loom Pattern Weaver[/bold green]\n"
        "[dim]Weaving OSS capabilities into emergent architectures[/dim]",
        title="Welcome"
    ))
    console.print("✅ Loom CLI is working!")

@app.command()
def demo():
    """Demonstrate the full power of Loom Pattern Weaver."""
    console.print(Panel.fit(
        "[bold green]🧵 LOOM PATTERN WEAVER DEMO[/bold green]\n"
        "[dim]From OSS threads to architectural tapestries[/dim]",
        title="Architectural Alchemy"
    ))
    
    graph = get_graph()
    stats = graph.get_stats()
    
    # Show what we have
    console.print("\n[bold]📚 Our Knowledge Base:[/bold]")
    console.print(f"  • [cyan]{stats['projects']}[/cyan] OSS projects")
    console.print(f"  • [green]{stats['edges']}[/green] compatibility relationships")
    console.print(f"  • [yellow]{stats['capability_coverage']}[/yellow] capability types")
    
    # Demo 1: ML Serving Pattern
    console.print("\n[bold]🤖 DEMO 1: ML Model Serving API[/bold]")
    intent1 = Intent(
        description="Serve machine learning models via API",
        required_capabilities=[CapabilityType.WEB_FRAMEWORK, CapabilityType.AI_MODEL],
        constraints={},
        priority="high"
    )
    
    weaver = PatternWeaver(graph)
    patterns1 = weaver.weave_for_intent(intent1)
    
    if patterns1:
        pattern = patterns1[0]
        console.print(f"  • Pattern: [cyan]{pattern.name}[/cyan]")
        console.print(f"  • Confidence: [green]{pattern.confidence:.3f}[/green]")
        console.print(f"  • Components: {', '.join([comp[0].name for comp in pattern.components])}")
    
    # Demo 2: Monitoring Stack
    console.print("\n[bold]📊 DEMO 2: Monitoring & Observability[/bold]")
    intent2 = Intent(
        description="Monitor web application performance",
        required_capabilities=[CapabilityType.WEB_FRAMEWORK, CapabilityType.MONITORING],
        constraints={},
        priority="medium"
    )
    
    patterns2 = weaver.weave_for_intent(intent2)
    if patterns2:
        pattern = patterns2[0]
        console.print(f"  • Pattern: [cyan]{pattern.name}[/cyan]")
        console.print(f"  • Confidence: [green]{pattern.confidence:.3f}[/green]")
    
    # Demo 3: Full Stack Web App
    console.print("\n[bold]🌐 DEMO 3: Full Stack Web Application[/bold]")
    intent3 = Intent(
        description="Production web application with database and cache",
        required_capabilities=[CapabilityType.WEB_FRAMEWORK, CapabilityType.DATABASE, CapabilityType.CACHE],
        constraints={},
        priority="high"
    )
    
    patterns3 = weaver.weave_for_intent(intent3)
    if patterns3:
        pattern = patterns3[0]
        console.print(f"  • Pattern: [cyan]{pattern.name}[/cyan]")
        console.print(f"  • Confidence: [green]{pattern.confidence:.3f}[/green]")
        console.print(f"  • Components: {len(pattern.components)} integrated services")
    
    # Show available commands
    console.print("\n[bold]🛠️  Available Commands:[/bold]")
    console.print("  • [cyan]loom weave[/cyan] - Create architectural patterns")
    console.print("  • [cyan]loom list-projects[/cyan] - Browse OSS projects")
    console.print("  • [cyan]loom search <query>[/cyan] - Find projects")
    console.print("  • [cyan]loom graph-stats[/cyan] - View knowledge graph")
    console.print("  • [cyan]loom add-real-world[/cyan] - Expand ecosystem")
    
    console.print("\n[bold green]✅ Loom is ready to weave your architectural visions![/bold green]")

@app.command()
def graph_stats():
    """Show statistics about the semantic graph."""
    graph = get_graph()
    stats = graph.get_stats()
    
    table = Table(title="Semantic Graph Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Projects", str(stats["projects"]))
    table.add_row("Nodes", str(stats["nodes"]))
    table.add_row("Edges", str(stats["edges"]))
    table.add_row("Capabilities Covered", str(stats["capability_coverage"]))
    
    console.print(table)

@app.command()
def add_sample():
    """Add sample OSS projects to the graph (for testing)."""
    graph = get_graph()
    console.print("[bold]Adding sample OSS projects...[/bold]")
    
    # Add some sample projects
    sample_projects = [
        OSSProject(
            name="FastAPI",
            description="Modern, fast web framework for building APIs with Python",
            capabilities=[CapabilityType.WEB_FRAMEWORK],
            license="MIT",
            popularity_score=0.9,
            compatibility_tags=["python", "async", "rest"]
        ),
        OSSProject(
            name="PostgreSQL",
            description="Powerful, open source object-relational database system",
            capabilities=[CapabilityType.DATABASE],
            license="PostgreSQL",
            popularity_score=0.95,
            compatibility_tags=["sql", "acid", "relational"]
        ),
        OSSProject(
            name="Redis",
            description="In-memory data structure store, used as database, cache, and message broker",
            capabilities=[CapabilityType.CACHE, CapabilityType.MESSAGE_QUEUE],
            license="BSD",
            popularity_score=0.85,
            compatibility_tags=["cache", "nosql", "key-value"]
        ),
        OSSProject(
            name="SQLAlchemy",
            description="Python SQL toolkit and Object Relational Mapper",
            capabilities=[CapabilityType.DATABASE],
            license="MIT",
            popularity_score=0.8,
            compatibility_tags=["python", "orm", "sql"]
        ),
    ]
    
    # Add relationships
    sample_relationships = [
        Relationship(
            source="FastAPI",
            target="SQLAlchemy",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.9,
            evidence="Commonly used together in Python web applications"
        ),
        Relationship(
            source="SQLAlchemy",
            target="PostgreSQL",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.95,
            evidence="SQLAlchemy has excellent PostgreSQL support"
        ),
        Relationship(
            source="FastAPI",
            target="PostgreSQL",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.85,
            evidence="Direct integration available"
        ),
        Relationship(
            source="Redis",
            target="FastAPI",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.8,
            evidence="Commonly used for caching in FastAPI apps"
        ),
        Relationship(
            source="Redis",
            target="PostgreSQL",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.7,
            evidence="Redis often caches PostgreSQL queries"
        ),
    ]
    
    # Add to graph
    for project in sample_projects:
        graph.add_project(project)
    
    for relationship in sample_relationships:
        graph.add_relationship(relationship)
    
    console.print("[green]✅ Sample data added![/green]")
    console.print("\nRun [bold]loom graph-stats[/bold] to see the graph statistics.")

@app.command()
def add_real_world():
    """Add real-world OSS projects for more diverse patterns."""
    graph = get_graph()
    console.print("[bold]Adding real-world OSS projects...[/bold]")
    
    # Real-world OSS projects
    real_projects = [
        # Web Frameworks
        OSSProject(
            name="Django",
            description="High-level Python Web framework that encourages rapid development",
            capabilities=[CapabilityType.WEB_FRAMEWORK],
            license="BSD",
            popularity_score=0.88,
            compatibility_tags=["python", "batteries-included", "orm"]
        ),
        OSSProject(
            name="Flask",
            description="Lightweight WSGI web application framework in Python",
            capabilities=[CapabilityType.WEB_FRAMEWORK],
            license="BSD",
            popularity_score=0.87,
            compatibility_tags=["python", "microframework", "simple"]
        ),
        OSSProject(
            name="Express.js",
            description="Fast, unopinionated, minimalist web framework for Node.js",
            capabilities=[CapabilityType.WEB_FRAMEWORK],
            license="MIT",
            popularity_score=0.92,
            compatibility_tags=["javascript", "nodejs", "minimalist"]
        ),
        
        # Databases
        OSSProject(
            name="MySQL",
            description="World's most popular open source database",
            capabilities=[CapabilityType.DATABASE],
            license="GPL",
            popularity_score=0.93,
            compatibility_tags=["sql", "relational", "enterprise"]
        ),
        OSSProject(
            name="MongoDB",
            description="Document-oriented NoSQL database",
            capabilities=[CapabilityType.DATABASE],
            license="SSPL",
            popularity_score=0.89,
            compatibility_tags=["nosql", "document", "json"]
        ),
        OSSProject(
            name="SQLite",
            description="C-language library that implements a small, fast, self-contained SQL database engine",
            capabilities=[CapabilityType.DATABASE],
            license="Public Domain",
            popularity_score=0.91,
            compatibility_tags=["embedded", "zero-config", "serverless"]
        ),
        
        # Caching & Message Queues
        OSSProject(
            name="RabbitMQ",
            description="Message broker that implements AMQP protocol",
            capabilities=[CapabilityType.MESSAGE_QUEUE],
            license="Mozilla Public License",
            popularity_score=0.82,
            compatibility_tags=["message-queue", "amqp", "enterprise"]
        ),
        OSSProject(
            name="Kafka",
            description="Distributed event streaming platform",
            capabilities=[CapabilityType.MESSAGE_QUEUE],
            license="Apache 2.0",
            popularity_score=0.86,
            compatibility_tags=["streaming", "distributed", "scalable"]
        ),
        
        # AI/ML
        OSSProject(
            name="TensorFlow",
            description="End-to-end open source platform for machine learning",
            capabilities=[CapabilityType.AI_MODEL],
            license="Apache 2.0",
            popularity_score=0.90,
            compatibility_tags=["ml", "deep-learning", "python"]
        ),
        OSSProject(
            name="PyTorch",
            description="Open source machine learning framework",
            capabilities=[CapabilityType.AI_MODEL],
            license="BSD",
            popularity_score=0.88,
            compatibility_tags=["ml", "research", "python"]
        ),
        
        # Monitoring
        OSSProject(
            name="Grafana",
            description="Open source analytics and monitoring solution",
            capabilities=[CapabilityType.MONITORING],
            license="AGPL",
            popularity_score=0.87,
            compatibility_tags=["visualization", "metrics", "dashboards"]
        ),
        OSSProject(
            name="Prometheus",
            description="Systems monitoring and alerting toolkit",
            capabilities=[CapabilityType.MONITORING],
            license="Apache 2.0",
            popularity_score=0.85,
            compatibility_tags=["metrics", "time-series", "kubernetes"]
        ),
    ]
    
    # Real-world relationships
    real_relationships = [
        # Django ecosystem
        Relationship(
            source="Django",
            target="PostgreSQL",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.9,
            evidence="Django has excellent built-in PostgreSQL support"
        ),
        Relationship(
            source="Django",
            target="MySQL",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.85,
            evidence="Django supports MySQL as a database backend"
        ),
        Relationship(
            source="Django",
            target="Redis",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.8,
            evidence="Django Redis cache backend available"
        ),
        
        # Flask ecosystem
        Relationship(
            source="Flask",
            target="SQLAlchemy",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.95,
            evidence="Flask-SQLAlchemy extension provides integration"
        ),
        Relationship(
            source="Flask",
            target="SQLite",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.9,
            evidence="Common choice for Flask development and prototyping"
        ),
        
        # Node.js ecosystem
        Relationship(
            source="Express.js",
            target="MongoDB",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.88,
            evidence="MEAN/MERN stack popular combination"
        ),
        Relationship(
            source="Express.js",
            target="Redis",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.82,
            evidence="Redis commonly used for sessions in Express.js"
        ),
        
        # AI/ML integrations
        Relationship(
            source="FastAPI",
            target="TensorFlow",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.75,
            evidence="FastAPI commonly used to serve ML models"
        ),
        Relationship(
            source="FastAPI",
            target="PyTorch",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.75,
            evidence="FastAPI used for ML model serving APIs"
        ),
        
        # Monitoring stack
        Relationship(
            source="Prometheus",
            target="Grafana",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.95,
            evidence="Standard monitoring stack combination"
        ),
        Relationship(
            source="FastAPI",
            target="Prometheus",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.7,
            evidence="Prometheus metrics for FastAPI applications"
        ),
        
        # Message queue integrations
        Relationship(
            source="FastAPI",
            target="RabbitMQ",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.72,
            evidence="Celery with RabbitMQ for background tasks"
        ),
        Relationship(
            source="Kafka",
            target="FastAPI",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.68,
            evidence="Event-driven architectures with Kafka"
        ),
    ]
    
    # Add to graph
    added_count = 0
    for project in real_projects:
        if project.name not in graph.projects:
            graph.add_project(project)
            added_count += 1
        else:
            console.print(f"[dim]Project {project.name} already exists, skipping[/dim]")
    
    for relationship in real_relationships:
        graph.add_relationship(relationship)
    
    console.print(f"[green]✅ Added {added_count} new real-world projects![/green]")
    console.print("\nNow you have a rich ecosystem for pattern weaving!")
    console.print("Try: loom weave --desc 'ML model serving API' --cap web_framework --cap ai_model")

@app.command(name="find-by-capability")
def find_by_capability(
    capability: str = typer.Argument(..., help="Capability to search for")
):
    """Find projects that provide a specific capability."""
    graph = get_graph()
    try:
        cap_type = CapabilityType(capability.lower())
        projects = graph.find_by_capability(cap_type)
        
        if projects:
            table = Table(title=f"Projects with capability: {capability}")
            table.add_column("Project Name", style="cyan")
            table.add_column("Description", style="dim")
            
            for project_name in projects:
                project = graph.projects.get(project_name)
                desc = project.description[:60] + "..." if len(project.description) > 60 else project.description
                table.add_row(project_name, desc)
            
            console.print(table)
        else:
            console.print(f"[yellow]No projects found with capability: {capability}[/yellow]")
    except ValueError:
        console.print(f"[red]Invalid capability: {capability}[/red]")
        console.print(f"Available capabilities: {[c.value for c in CapabilityType]}")

@app.command()
def graph_clear():
    """Clear all data from the semantic graph."""
    graph = get_graph()
    graph.clear()
    console.print("[green]✅ Semantic graph cleared![/green]")

@app.command(name="list-projects")
def list_projects():
    """List all projects in the semantic graph."""
    graph = get_graph()
    projects = list(graph.projects.keys())
    
    if projects:
        table = Table(title="OSS Projects in Semantic Graph")
        table.add_column("Name", style="cyan")
        table.add_column("Capabilities", style="green")
        table.add_column("License", style="yellow")
        
        for name in sorted(projects):
            project = graph.projects.get(name)
            caps = ", ".join([c.value for c in project.capabilities])
            table.add_row(name, caps, project.license or "Unknown")
        
        console.print(table)
        console.print(f"[dim]Total: {len(projects)} projects[/dim]")
    else:
        console.print("[yellow]No projects in the graph. Run 'loom add-sample' to add some.[/yellow]")

@app.command(name="show-project")
def show_project(
    name: str = typer.Argument(..., help="Project name to show details for")
):
    """Show detailed information about a specific project."""
    graph = get_graph()
    
    if name not in graph.projects:
        console.print(f"[red]Project '{name}' not found in graph.[/red]")
        return
    
    project = graph.projects[name]
    
    # Create a detailed panel
    console.print(Panel.fit(
        f"[bold]{project.name}[/bold]\n"
        f"[dim]{project.description}[/dim]",
        title="Project Details",
        border_style="cyan"
    ))
    
    # Create a table with details
    info_table = Table(show_header=False)
    info_table.add_row("License", f"[yellow]{project.license or 'Unknown'}[/yellow]")
    info_table.add_row("Popularity", f"[green]{project.popularity_score}[/green]")
    info_table.add_row("Tags", f"[dim]{', '.join(project.compatibility_tags)}[/dim]")
    
    capabilities = ", ".join([f"[cyan]{c.value}[/cyan]" for c in project.capabilities])
    info_table.add_row("Capabilities", capabilities)
    
    console.print(info_table)
    
    # Show compatible projects
    compatible = graph.get_compatible_projects(name)
    if compatible:
        console.print("\n[bold]Compatible with:[/bold]")
        for comp in compatible:
            console.print(f"  • [green]{comp}[/green]")

@app.command(name="search")
def search_projects(
    query: str = typer.Argument(..., help="Search query")
):
    """Search for projects by name, description, or tags."""
    graph = get_graph()
    results = graph.search(query)
    
    if results:
        table = Table(title=f"Search Results for: '{query}'")
        table.add_column("Project", style="cyan")
        table.add_column("Description", style="dim")
        
        for name in results:
            project = graph.projects.get(name)
            desc = project.description[:80] + "..." if len(project.description) > 80 else project.description
            table.add_row(name, desc)
        
        console.print(table)
        console.print(f"[dim]Found {len(results)} results[/dim]")
    else:
        console.print(f"[yellow]No projects found matching '{query}'[/yellow]")

@app.command(name="weave")
def weave_pattern(
    description: str = typer.Option(..., "--desc", "-d", help="Description of what you want to build"),
    capabilities: Optional[List[str]] = typer.Option(None, "--cap", "-c", help="Required capabilities"),
    save: Optional[str] = typer.Option(None, "--save", "-s", help="Save pattern as JSON file")
):
    """
    Weave an architectural pattern based on your requirements.
    
    Example: loom weave --desc "A web API with database" --cap web_framework --cap database
    """
    graph = get_graph()
    console.print(Panel.fit("[bold]🧵 Weaving Patterns...[/bold]", border_style="green"))
    
    # Parse capabilities
    required_caps = []
    if capabilities:
        for cap_str in capabilities:
            try:
                cap_type = CapabilityType(cap_str.lower())
                required_caps.append(cap_type)
            except ValueError:
                console.print(f"[yellow]Warning: Invalid capability '{cap_str}', skipping[/yellow]")
    
    # Create intent
    intent = Intent(
        description=description,
        required_capabilities=required_caps,
        constraints={},
        priority="medium"
    )
    
    console.print(f"[dim]Intent:[/dim] {description}")
    if required_caps:
        console.print(f"[dim]Required:[/dim] {[c.value for c in required_caps]}")
    
    # Weave patterns
    weaver = PatternWeaver(graph)
    patterns = weaver.weave_for_intent(intent)
    
    if not patterns:
        console.print("[yellow]No patterns found for your requirements.[/yellow]")
        console.print("Try adding more projects with 'loom add-sample' or specify different capabilities.")
        return
    
    # Display patterns
    console.print(f"\n[bold]Found {len(patterns)} pattern(s):[/bold]")
    
    for i, pattern_dict in enumerate(weaver.get_all_patterns()):
        pattern_num = i + 1
        
        # Pattern header with metrics
        console.print(Panel.fit(
            f"[bold cyan]Pattern {pattern_num}: {pattern_dict['name']}[/bold cyan]\n"
            f"[dim]{pattern_dict['description']}[/dim]\n"
            f"Confidence: [green]{pattern_dict['confidence']:.3f}[/green] | "
            f"Complexity: [yellow]{pattern_dict['complexity']:.3f}[/yellow]",
            border_style="cyan"
        ))
        
        # Components table
        comp_table = Table(title="Components")
        comp_table.add_column("Role", style="yellow", width=20)
        comp_table.add_column("Project", style="green")
        comp_table.add_column("Capabilities", style="cyan")
        comp_table.add_column("Popularity", style="dim", justify="right")
        
        for comp in pattern_dict["components"]:
            comp_table.add_row(
                comp["role"],
                comp["name"],
                ", ".join(comp["capabilities"]),
                f"{comp['popularity']:.2f}"
            )
        
        console.print(comp_table)
        
        # Connections
        if pattern_dict["connections"]:
            conn_table = Table(title="Connections")
            conn_table.add_column("From → To", style="dim")
            conn_table.add_column("Type", style="cyan")
            conn_table.add_column("Strength", style="green", justify="right")
            
            for conn in pattern_dict["connections"]:
                conn_table.add_row(
                    f"{conn['from']} → {conn['to']}",
                    conn["type"],
                    f"{conn['strength']:.2f}"
                )
            
            console.print(conn_table)
        
        # Save if requested
        if save and i == 0:  # Save first pattern
            filename = f"{save}.json" if not save.endswith('.json') else save
            with open(filename, 'w') as f:
                json.dump(pattern_dict, f, indent=2)
            console.print(f"[green]✅ Pattern saved to {filename}[/green]")
        
        console.print()  # Empty line between patterns

# Create a callable entry point
def run():
    app()

if __name__ == "__main__":
    run()

@app.command(name="generate")
def generate_code(
    pattern_file: str = typer.Argument(..., help="JSON pattern file to generate code from"),
    output_dir: str = typer.Option("./loom_output", "--output", "-o", help="Output directory")
):
    """Generate deployable code from a saved pattern."""
    from pathlib import Path
    console.print(Panel.fit("[bold]⚡ Generating Code...[/bold]", border_style="blue"))
    
    pattern_path = Path(pattern_file)
    if not pattern_path.exists():
        console.print(f"[red]Pattern file not found: {pattern_file}[/red]")
        return
    
    # Load pattern
    with open(pattern_path, 'r') as f:
        pattern_dict = json.load(f)
    
    console.print(f"[dim]Pattern:[/dim] {pattern_dict['name']}")
    
    # Generate code
    from .generator import ManifestGenerator
    generator = ManifestGenerator()
    generated_files = generator.generate_from_pattern(pattern_dict, output_dir)
    
    console.print(f"[green]✅ Generated in: {output_dir}[/green]")
    console.print("Files created:")
    for file_type, file_path in generated_files.items():
        console.print(f"  • {Path(file_path).name}")
    
    console.print(f"\n🚀 Run: [cyan]cd {output_dir} && docker-compose up -d[/cyan]")

@app.command()
def add_missing_projects():
    """Add critical missing OSS projects for real-world scenarios."""
    graph = get_graph()
    console.print("[bold]Adding critical missing OSS projects...[/bold]")
    
    missing_projects = [
        # Storage & File Handling
        OSSProject(
            name="MinIO",
            description="High Performance Object Storage, API compatible with Amazon S3",
            capabilities=[CapabilityType.STORAGE, CapabilityType.OBJECT_STORAGE],
            license="Apache 2.0",
            popularity_score=0.82,
            compatibility_tags=["s3", "cloud", "storage", "go"]
        ),
        
        # Authentication & Security
        OSSProject(
            name="Keycloak",
            description="Open Source Identity and Access Management for Modern Applications",
            capabilities=[CapabilityType.AUTHENTICATION],
            license="Apache 2.0",
            popularity_score=0.85,
            compatibility_tags=["sso", "oauth", "security", "java"]
        ),
        
        # Search Engines
        OSSProject(
            name="Elasticsearch",
            description="Distributed, RESTful Search and Analytics Engine",
            capabilities=[CapabilityType.SEARCH],
            license="Elastic License",
            popularity_score=0.88,
            compatibility_tags=["search", "analytics", "lucene", "java"]
        ),
        OSSProject(
            name="MeiliSearch",
            description="Powerful, fast, open source, easy to use search engine",
            capabilities=[CapabilityType.SEARCH],
            license="MIT",
            popularity_score=0.75,
            compatibility_tags=["search", "instant", "rust", "simple"]
        ),
        
        # Load Balancing & Proxy
        OSSProject(
            name="NGINX",
            description="High performance load balancer, web server, & reverse proxy",
            capabilities=[CapabilityType.LOAD_BALANCER],
            license="BSD",
            popularity_score=0.95,
            compatibility_tags=["proxy", "webserver", "c", "high-performance"]
        ),
        
        # Email Services
        OSSProject(
            name="Postfix",
            description="Fast, easy to administer, secure Sendmail replacement",
            capabilities=[CapabilityType.EMAIL],
            license="IBM Public License",
            popularity_score=0.80,
            compatibility_tags=["smtp", "mail", "c", "reliable"]
        ),
    ]
    
    # Add compatibility relationships
    missing_relationships = [
        # Web frameworks work with these services
        Relationship(
            source="FastAPI",
            target="MinIO",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.7,
            evidence="FastAPI can integrate with MinIO for file uploads/downloads"
        ),
        Relationship(
            source="Django",
            target="MinIO",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.8,
            evidence="Django has packages for MinIO integration"
        ),
        Relationship(
            source="FastAPI",
            target="Keycloak",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.75,
            evidence="FastAPI-Keycloak integration available"
        ),
        Relationship(
            source="Express.js",
            target="Keycloak",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.8,
            evidence="Keycloak Node.js adapter available"
        ),
        Relationship(
            source="FastAPI",
            target="Elasticsearch",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.7,
            evidence="Elasticsearch Python client works with FastAPI"
        ),
        Relationship(
            source="FastAPI",
            target="NGINX",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.9,
            evidence="Standard deployment: NGINX as reverse proxy for FastAPI"
        ),
        
        # Databases work with search engines
        Relationship(
            source="PostgreSQL",
            target="Elasticsearch",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.75,
            evidence="Common pattern: PostgreSQL for data, Elasticsearch for search"
        ),
        Relationship(
            source="MongoDB",
            target="Elasticsearch",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.8,
            evidence="MongoDB connector for Elasticsearch available"
        ),
        
        # Storage works with everything
        Relationship(
            source="MinIO",
            target="FastAPI",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.7,
            evidence="MinIO Python SDK works with FastAPI"
        ),
        Relationship(
            source="MinIO",
            target="Django",
            relationship_type=RelationshipType.COMPATIBLE_WITH,
            strength=0.75,
            evidence="django-minio-storage package available"
        ),
    ]
    
    # Add projects
    added_count = 0
    for project in missing_projects:
        if project.name not in graph.projects:
            graph.add_project(project)
            added_count += 1
        else:
            console.print(f"[dim]Project {project.name} already exists[/dim]")
    
    # Add relationships
    for relationship in missing_relationships:
        graph.add_relationship(relationship)
    
    console.print(f"[green]✅ Added {added_count} critical missing projects![/green]")
    console.print("\nNow Loom understands: Storage, Authentication, Search, Load Balancing, Email!")
