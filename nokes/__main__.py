"""Nokes package entry point"""

import sys

if len(sys.argv) > 1 and sys.argv[1] == "server":
    from nokes.api.server import create_app
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
elif len(sys.argv) > 1 and sys.argv[1] == "cli":
    from nokes.cli.main import cli
    cli()
else:
    print("Nokes AI v0.1.0")
    print("")
    print("Usage:")
    print("  python -m nokes server     Run API server")
    print("  python -m nokes cli        Run CLI interface")
    print("")
