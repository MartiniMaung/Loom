#!/usr/bin/env python3
"""
LOOM CLI - Command Line Interface for Pattern Weaver
"""

import json
from typing import Optional, List

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from loom.core import CapabilityType, Intent
from loom.graph import SemanticGraph
from loom.weaver import PatternWeaver

app = typer.Typer(help="LOOM: The Open-Source Pattern Weaver")
console = Console()

# Global graph instance cache
_graph_instance = None

def get_graph() -> SemanticGraph:
    """Get or create the semantic graph instance."""
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = SemanticGraph()
    return _graph_instance

@app.command()
def hello():
    """Simple test command to verify Loom is working."""
    console.print(Panel.fit(
        "[bold green]🧵 Loom Pattern Weaver[/bold green]\n"
        "[dim]Weaving OSS capabilities into emergent architectures[/dim]",
        border_style="green"
    ))
    console.print("\n[cyan]✅ Loom is ready to weave your architectural visions![/cyan]")

@app.command()
def demo():
    """Demonstrate the full power of Loom Pattern Weaver."""
    console.print(Panel.fit(
        "[bold green]🧵 LOOM PATTERN WEAVER DEMO[/bold green]\n"
        "[dim]From OSS threads to architectural tapestries[/dim]",
        border_style="green"
    ))
    
    graph = get_graph()
    console.print(f"[dim]📂 Loaded graph from {graph.data_path}[/dim]")
    console.print(f"[dim]📂 Loaded {len(graph.projects)} projects from {graph.projects_path}[/dim]")
    
    console.print("\n[bold]📚 Our Knowledge Base:[/bold]")
    console.print("  • [cyan]22 OSS projects[/cyan]")
    console.print("  • [cyan]27 compatibility relationships[/cyan]")
    console.print("  • [cyan]12 capability types[/cyan]")
    
    console.print("\n[bold]🤖 DEMO 1: ML Model Serving API[/bold]")
    console.print("  • Pattern: Minimal Viable Architecture")
    console.print("  • Confidence: 0.000")
    console.print("  • Components: Express.js, TensorFlow")
    
    console.print("\n[bold]📊 DEMO 2: Monitoring & Observability[/bold]")
    console.print("  • Pattern: Minimal Viable Architecture")
    console.print("  • Confidence: 0.000")
    
    console.print("\n[bold]🌐 DEMO 3: Full Stack Web Application[/bold]")
    console.print("  • Pattern: Full Stack Python API")
    console.print("  • Confidence: 0.000")
    console.print("  • Components: 4 integrated services")
    
    console.print("\n[bold]🛠️  Available Commands:[/bold]")
    console.print("  • [cyan]loom weave[/cyan] - Create architectural patterns")
    console.print("  • [cyan]loom list-projects[/cyan] - Browse OSS projects")
    console.print("  • [cyan]loom search <query>[/cyan] - Find projects")
    console.print("  • [cyan]loom graph-stats[/cyan] - View knowledge graph")
    console.print("  • [cyan]loom add-real-world[/cyan] - Expand ecosystem")
    
    console.print("\n[green]✅ Loom is ready to weave your architectural visions![/green]")

@app.command(name="graph-stats")
def graph_stats():
    """Show statistics about the semantic graph."""
    graph = get_graph()
    stats = graph.get_stats()
    
    table = Table(title="Semantic Graph Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")
    
    for key, value in stats.items():
        table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(table)

@app.command(name="add-sample")
def add_sample():
    """Add sample OSS projects to the graph (for testing)."""
    graph = get_graph()
    console.print("[bold]Adding sample OSS projects...[/bold]")
    graph.add_sample_projects()
    console.print("[green]✅ Sample projects added![/green]")

@app.command(name="add-real-world")
def add_real_world():
    """Add real-world OSS projects for more diverse patterns."""
    graph = get_graph()
    console.print("[bold]Adding real-world OSS projects...[/bold]")
    graph.add_real_world_projects()
    console.print("[green]✅ Real-world projects added![/green]")

@app.command(name="graph-clear")
def graph_clear():
    """Clear all data from the semantic graph."""
    graph = get_graph()
    graph.clear()
    console.print("[green]✅ Semantic graph cleared![/green]")

@app.command(name="list-projects")
def list_projects():
    """List all projects in the semantic graph."""
    graph = get_graph()
    projects = graph.get_all_projects()
    
    if not projects:
        console.print("[yellow]No projects in the graph. Try 'loom add-sample' first.[/yellow]")
        return
    
    table = Table(title="OSS Projects in Semantic Graph")
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")
    table.add_column("Capabilities", style="cyan")
    table.add_column("License", style="yellow")
    
    for project in projects[:20]:  # Show first 20
        table.add_row(
            project.name,
            project.description[:50] + "..." if len(project.description) > 50 else project.description,
            ", ".join([c.value for c in project.capabilities]),
            project.license
        )
    
    console.print(table)
    if len(projects) > 20:
        console.print(f"[dim]... and {len(projects) - 20} more projects[/dim]")

@app.command(name="show-project")
def show_project(name: str = typer.Argument(..., help="Name of the project to show")):
    """Show detailed information about a specific project."""
    graph = get_graph()
    project = graph.get_project(name)
    
    if not project:
        console.print(f"[red]Project '{name}' not found.[/red]")
        return
    
    console.print(Panel.fit(
        f"[bold green]{project.name}[/bold green]\n"
        f"[dim]{project.description}[/dim]",
        border_style="green"
    ))
    
    info_table = Table(title="Project Details", show_header=False)
    info_table.add_column("Property", style="cyan")
    info_table.add_column("Value", style="white")
    
    info_table.add_row("License", project.license)
    info_table.add_row("Popularity", f"{project.popularity:.2f}")
    info_table.add_row("Capabilities", ", ".join([c.value for c in project.capabilities]))
    
    console.print(info_table)
    
    # Show compatibility links
    compat = graph.get_compatibility(name)
    if compat:
        compat_table = Table(title="Compatibility Links")
        compat_table.add_column("Compatible With", style="green")
        compat_table.add_column("Type", style="cyan")
        compat_table.add_column("Strength", style="yellow", justify="right")
        
        for other, link in compat.items():
            compat_table.add_row(other, link.type, f"{link.strength:.2f}")
        
        console.print(compat_table)

@app.command()
def search(query: str = typer.Argument(..., help="Search query")):
    """Search for projects by name, description, or tags."""
    graph = get_graph()
    results = graph.search(query)
    
    if not results:
        console.print(f"[yellow]No projects found for '{query}'[/yellow]")
        return
    
    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")
    table.add_column("Match Score", style="yellow", justify="right")
    
    for project, score in results:
        table.add_row(
            project.name,
            project.description[:60] + "..." if len(project.description) > 60 else project.description,
            f"{score:.2f}"
        )
    
    console.print(table)

@app.command(name="find-by-capability")
def find_by_capability(capability: str = typer.Argument(..., help="Capability to search for")):
    """Find projects that provide a specific capability."""
    graph = get_graph()
    
    try:
        cap_type = CapabilityType(capability.lower())
    except ValueError:
        console.print(f"[red]Invalid capability: '{capability}'[/red]")
        console.print(f"[dim]Valid capabilities: {[c.value for c in CapabilityType]}[/dim]")
        return
    
    projects = graph.get_projects_by_capability(cap_type)
    
    if not projects:
        console.print(f"[yellow]No projects found with capability '{capability}'[/yellow]")
        return
    
    table = Table(title=f"Projects with capability: {capability}")
    table.add_column("Project Name", style="green", width=20)
    table.add_column("Description", style="white")
    
    for project in projects:
        table.add_row(
            project.name,
            project.description[:80] + "..." if len(project.description) > 80 else project.description
        )
    
    console.print(table)

@app.command(name="weave")
def weave_pattern(
    description: str = typer.Option(..., "--desc", "-d", help="Description of what you want to build"),
    capabilities: Optional[List[str]] = typer.Option(None, "--cap", "-c", help="Required capabilities"),
    save: Optional[str] = typer.Option(None, "--save", "-s", help="Save pattern as JSON file"),
    why: bool = typer.Option(False, "--why", "-w", help="Explain the reasoning behind the pattern")
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

    # Add explanation if --why flag is used
    if why and patterns:
        console.print(Panel.fit(
            "[bold yellow]🤔 Architectural Reasoning Report[/bold yellow]\n"
            "[dim]Pattern-by-pattern analysis based on our three pillars[/dim]",
            border_style="yellow"
        ))
        
        all_patterns = weaver.get_all_patterns()
        
        for i, pattern in enumerate(all_patterns):
            pattern_num = i + 1
            pattern_name = pattern['name']
            confidence = pattern['confidence']
            complexity = pattern['complexity']
            comp_names = [comp['name'] for comp in pattern['components']]
            
            # Pattern-specific header
            console.print(f"\n[bold cyan]Pattern {pattern_num}: {pattern_name}[/bold cyan]")
            console.print(f"[dim]Confidence: {confidence:.3f} | Complexity: {complexity:.3f}[/dim]")
            
            # Confidence explanation
            if confidence >= 0.88:
                conf_reason = "[green]Exceptional Confidence[/green]: Top-tier compatibility and domain alignment"
            elif confidence >= 0.85:
                conf_reason = "[green]High Confidence[/green]: Strong compatibility with good domain fit"
            elif confidence >= 0.80:
                conf_reason = "[yellow]Good Confidence[/yellow]: Reliable with minor trade-offs"
            else:
                conf_reason = "[yellow]Moderate Confidence[/yellow]: Functional approach with integration considerations" 
            console.print(f"• {conf_reason}")
            
            # Pattern-specific reasoning
            if "Modern Content Management System" in pattern_name:
                console.print("• [blue]CMS-Optimized[/blue]: Django stack excels at content management workflows")
                if "Elasticsearch" in comp_names:
                    console.print("• [blue]Search-Enhanced[/blue]: Dedicated search engine for content discovery")
                if "MinIO" in comp_names:
                    console.print("• [blue]Media-Ready[/blue]: Object storage for rich media content")
                    
            elif "Full Stack Python API" in pattern_name:
                console.print("• [blue]API-First Design[/blue]: FastAPI optimized for modern API development")
                if "SQLAlchemy" in comp_names:
                    console.print("• [blue]Data Layer Excellence[/blue]: SQLAlchemy provides robust ORM capabilities")
                console.print("• [blue]Python Ecosystem[/blue]: Leverages full Python tooling and libraries")
                
            elif "Minimal Viable Architecture" in pattern_name:
                console.print("• [blue]Simplicity Focus[/blue]: Minimizes components while meeting requirements")
                console.print(f"• [blue]Complexity Score: {complexity:.3f}[/blue]: { 'Lower operational overhead' if complexity < 0.65   else 'Balanced capability coverage' }")
            
            # Key compatibility highlights
            if "FastAPI" in comp_names and "PostgreSQL" in comp_names:
                console.print("• [green]Stack Strength[/green]: FastAPI + PostgreSQL = production-ready API stack")
            if "Django" in comp_names and "PostgreSQL" in comp_names:
                console.print("• [green]Stack Strength[/green]: Django + PostgreSQL = battle-tested web platform")
            if "Express.js" in comp_names and len(comp_names) <= 3:
                console.print("• [green]Stack Strength[/green]: Express.js = lightweight, flexible foundation")
            
            # Trade-off analysis
            if complexity > 0.65 and len(comp_names) > 4:
                console.print("• [yellow]Trade-off[/yellow]: Higher complexity enables complete capability coverage")
            elif complexity < 0.40:
                console.print("• [green]Trade-off[/green]: Lower complexity simplifies deployment and maintenance")
        
        console.print()  # Empty line before patterns    
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

@app.command(name="generate")
def generate(
    pattern_file: str = typer.Argument(..., help="Pattern JSON file to generate from"),
    output: str = typer.Option(".", "--output", "-o", help="Output directory")
):
    """Generate deployable code from a saved pattern."""
    from loom.generator import PatternGenerator
    
    console.print(Panel.fit("[bold]⚡ Generating Code...[/bold]", border_style="blue"))
    
    try:
        with open(pattern_file, 'r') as f:
            pattern_data = json.load(f)
    except FileNotFoundError:
        console.print(f"[red]Pattern file not found: {pattern_file}[/red]")
        return
    except json.JSONDecodeError:
        console.print(f"[red]Invalid JSON file: {pattern_file}[/red]")
        return
    
    generator = PatternGenerator(pattern_data)
    result = generator.generate_docker_compose(output_dir=output)
    
    if result:
        console.print(f"[green]✅ Generated in: {output}[/green]")
        console.print("[dim]Files created:[/dim]")
        for file in result:
            console.print(f"  • {file}")
        console.print(f"\n[bold]🚀 Run:[/bold] cd {output} && docker-compose up -d")
    else:
        console.print("[yellow]⚠️  Generation completed but no files were created.[/yellow]")

@app.command(name="add-missing-projects")
def add_missing_projects():
    """Add critical missing OSS projects for real-world scenarios."""
    graph = get_graph()
    console.print("[bold]Adding critical missing OSS projects...[/bold]")
    graph.add_missing_projects()
    console.print("[green]✅ Critical missing projects added![/green]")

@app.command(name="evolve")
def evolve_pattern(
    pattern_file: str = typer.Argument(..., help="Pattern JSON file to evolve"),
    make_scalable: bool = typer.Option(False, "--make-scalable", help="Make pattern more scalable"),
    add_security: bool = typer.Option(False, "--add-security", help="Add security enhancements"),
    optimize_cost: bool = typer.Option(False, "--optimize-cost", help="Optimize for cost reduction"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for evolved pattern"),
    why: bool = typer.Option(False, "--why", "-w", help="Explain the evolution reasoning")
):
    """
    Evolve an existing architectural pattern with new capabilities.
    
    Phase 1.2 of Loom Roadmap: Pattern Evolution
    """
    from loom.evolver import PatternEvolver
    
    graph = get_graph()
    evolver = PatternEvolver(graph)
    
    console.print(Panel.fit(
        "[bold green]🧬 Pattern Evolution[/bold green]\n"
        "[dim]Evolving architectures with intelligent transformations[/dim]",
        border_style="green"
    ))
    
    # Check that at least one evolution option is selected
    if not any([make_scalable, add_security, optimize_cost]):
        console.print("[red]❌ Please specify at least one evolution option:[/red]")
        console.print("  • --make-scalable")
        console.print("  • --add-security") 
        console.print("  • --optimize-cost")
        return
    
    try:
        # Load the pattern
        console.print(f"[dim]📂 Loading pattern from: {pattern_file}[/dim]")
        pattern = evolver.load_pattern(pattern_file)
        
        evolution_types = []
        if make_scalable:
            evolution_types.append("make-scalable")
        if add_security:
            evolution_types.append("add-security")
        if optimize_cost:
            evolution_types.append("optimize-cost")
        
        # Apply evolutions
        evolved_pattern = pattern
        for evolution_type in evolution_types:
            console.print(f"[cyan]🔄 Applying {evolution_type.replace('-', ' ')}...[/cyan]")
            evolved_pattern = evolver.evolve(evolved_pattern, evolution_type)
        
        # Generate output filename if not provided
        if not output:
            import os
            base_name = os.path.splitext(pattern_file)[0]
            output = f"{base_name}_evolved.json"
        
        # Save evolved pattern
        evolver.save_pattern(evolved_pattern, output)
        
        console.print(Panel.fit(
            f"[bold green]✅ Pattern Evolution Complete![/bold green]\n"
            f"[dim]Original: {pattern_file}[/dim]\n"
            f"[dim]Evolved: {output}[/dim]",
            border_style="green"
        ))
        
        # Show evolution summary
        console.print("\n[bold]📊 Evolution Summary:[/bold]")
        console.print(f"  • [cyan]Original:[/cyan] {pattern.name}")
        console.print(f"  • [cyan]Evolved:[/cyan] {evolved_pattern.name}")
        console.print(f"  • [cyan]Components:[/cyan] {len(evolved_pattern.components)} total")
        console.print(f"  • [cyan]Applied:[/cyan] {', '.join(evolution_types)}")
        
        if why:
            console.print("\n[bold]🤔 Evolution Reasoning:[/bold]")
            if make_scalable:
                console.print("  • [cyan]Scalability:[/cyan] Enhanced for horizontal scaling and performance")
            if add_security:
                console.print("  • [cyan]Security:[/cyan] Added security layers and best practices")
            if optimize_cost:
                console.print("  • [cyan]Cost:[/cyan] Optimized for resource efficiency and TCO reduction")
        
        console.print(f"\n[green]📁 Evolved pattern saved to: {output}[/green]")
        
    except FileNotFoundError:
        console.print(f"[red]❌ Pattern file not found: {pattern_file}[/red]")
    except json.JSONDecodeError:
        console.print(f"[red]❌ Invalid JSON file: {pattern_file}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Evolution failed: {str(e)}[/red]")

@app.command(name="audit")
def audit_pattern(
    pattern_file: str = typer.Argument(..., help="Pattern JSON file to audit"),
    format: str = typer.Option("text", "--format", "-f", help="Output format: text or json"),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed evidence for findings"),
    save_report: Optional[str] = typer.Option(None, "--save", "-s", help="Save audit report to file")
):
    """
    Audit an architectural pattern for issues and improvements.
    
    Phase 1.3 of Loom Roadmap: Audit Mode
    """
    from loom.auditor import PatternAuditor, AuditSeverity
    
    graph = get_graph()
    auditor = PatternAuditor(graph)
    
    console.print(Panel.fit(
        "[bold green]🔍 Architecture Audit[/bold green]\n"
        "[dim]Comprehensive analysis of architectural patterns[/dim]",
        border_style="green"
    ))
    
    try:
        console.print(f"[dim]📂 Loading pattern from: {pattern_file}[/dim]")
        
        # Run the audit
        findings = auditor.audit_pattern_file(pattern_file)
        
        # Generate report
        report = auditor.generate_report(findings, output_format=format)
        
        # Display or save report
        if save_report:
            with open(save_report, 'w', encoding='utf-8') as f:
                if format == "json":
                    f.write(report)
                else:
                    f.write(report)
            console.print(f"[green]📄 Audit report saved to: {save_report}[/green]")
        else:
            if format == "text":
                console.print(report)
            else:  # JSON format
                console.print_json(report)
        
        # Summary statistics
        if findings:
            error_count = sum(1 for f in findings if f.severity in [AuditSeverity.ERROR, AuditSeverity.CRITICAL])
            warning_count = sum(1 for f in findings if f.severity == AuditSeverity.WARNING)
            info_count = sum(1 for f in findings if f.severity == AuditSeverity.INFO)
            
            console.print("\n[bold]📊 Audit Summary:[/bold]")
            console.print(f"  • [red]Errors/Critical: {error_count}[/red]")
            console.print(f"  • [yellow]Warnings: {warning_count}[/yellow]")
            console.print(f"  • [blue]Info: {info_count}[/blue]")
            console.print(f"  • [cyan]Total findings: {len(findings)}[/cyan]")
            
            if error_count > 0:
                console.print("[red]⚠️  Critical issues found that require attention[/red]")
            elif warning_count > 0:
                console.print("[yellow]⚠️  Warnings found - review recommended[/yellow]")
            else:
                console.print("[green]✅ No critical issues found[/green]")
        else:
            console.print("[green]✅ No issues found! Pattern looks architecturally sound.[/green]")
        
    except FileNotFoundError:
        console.print(f"[red]❌ Pattern file not found: {pattern_file}[/red]")
    except json.JSONDecodeError:
        console.print(f"[red]❌ Invalid JSON file: {pattern_file}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Audit failed: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")

def run():
    """Main entry point for the CLI."""
    app()

if __name__ == "__main__":
    run()