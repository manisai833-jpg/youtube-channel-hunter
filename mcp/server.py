"""FastMCP server entry point for the YouTube Channel Hunter project."""

import importlib.util
import site
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

# Remove the project root from the import path so the installed MCP runtime can be loaded
# as the top-level package that FastMCP expects.
if str(project_root) in sys.path:
    sys.path.remove(str(project_root))

# Load the installed MCP runtime as the top-level 'mcp' package before importing FastMCP.
package_dir = None
for candidate in site.getsitepackages():
    candidate_path = Path(candidate) / "mcp"
    if candidate_path.is_dir() and (candidate_path / "__init__.py").exists():
        package_dir = candidate_path
        break

if package_dir is None:
    raise ImportError("Installed MCP package was not found")

mcp_spec = importlib.util.spec_from_file_location(
    "mcp",
    package_dir / "__init__.py",
    submodule_search_locations=[str(package_dir)],
)
if mcp_spec is None or mcp_spec.loader is None:
    raise ImportError("Unable to load the installed MCP package")

mcp_module = importlib.util.module_from_spec(mcp_spec)
sys.modules["mcp"] = mcp_module
mcp_spec.loader.exec_module(mcp_module)

from fastmcp import FastMCP

# Load the local tool module directly from file to avoid package-name collisions.
tools_path = project_root / "mcp" / "tools.py"
tools_spec = importlib.util.spec_from_file_location("mcp_tools", tools_path)
if tools_spec is None or tools_spec.loader is None:
    raise ImportError("Unable to load tool module")

tools_module = importlib.util.module_from_spec(tools_spec)
tools_spec.loader.exec_module(tools_module)

# Create the FastMCP application instance.
app = FastMCP("YouTube Channel Hunter")

# Register MCP tools with the application.
app.tool()(tools_module.search_youtube)


if __name__ == "__main__":
    app.run()
