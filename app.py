from pathlib import Path

from flask import Flask, abort, jsonify, render_template, send_from_directory


ROOT = Path(__file__).parent
app = Flask(__name__, static_folder=None)

SITE = {
    "name": "fyr.js",
    "package": "@aldane-dev-create/fyr",
    "version": "0.1.2",
    "email": "aldanehutchinson5@gmail.com",
    "phone": "876-561-6141",
}

NAVIGATION = [
    ("Docs", "docs_index"),
    ("Examples", "examples_index"),
    ("Blog", "blog_index"),
    ("Community", "community"),
    ("About", "about"),
]

DOCS = {
    "getting-started": {
        "title": "Getting started",
        "summary": "Create your first reactive Fyr application with plain HTML and an ES module import.",
        "sections": [
            {
                "heading": "Start with HTML",
                "body": "Give a page region a Fyr application name, then bind state to the markup with directives.",
                "code": '<div fyr-app="welcome">\n  <p fyr-text="message"></p>\n  <button fyr-click="changeMessage()">Change message</button>\n</div>',
            },
            {
                "heading": "Create and mount the application",
                "body": "Fyr is published as an ES module. Pin the package version in production.",
                "code": 'import { Fyr } from "https://cdn.jsdelivr.net/npm/@aldane-dev-create/fyr@0.1.2/dist/fyr.esm.js";\n\nFyr.createApp("welcome", {\n  state: { message: "Hello from Fyr" },\n  methods: {\n    changeMessage() {\n      this.state.message = "State updated.";\n    }\n  }\n});\n\nFyr.start("welcome");',
            },
        ],
    },
    "installation": {
        "title": "Installation",
        "summary": "Use Fyr directly from jsDelivr, install it from npm, or self-host the built distribution.",
        "sections": [
            {
                "heading": "CDN import",
                "body": "All Fyr browser bundles are ES modules, including minified files. Use type=module rather than a classic script tag.",
                "code": '<script type="module">\n  import { Fyr } from "https://cdn.jsdelivr.net/npm/@aldane-dev-create/fyr@0.1.2/dist/fyr.esm.js";\n</script>',
            },
            {
                "heading": "npm",
                "body": "Use the scoped package in projects that have their own build pipeline.",
                "code": 'npm install @aldane-dev-create/fyr\n\nimport { Fyr } from "@aldane-dev-create/fyr";',
            },
        ],
    },
    "reactivity": {
        "title": "Reactivity",
        "summary": "Fyr tracks state changes and updates bindings in the DOM without a virtual-DOM layer.",
        "sections": [
            {
                "heading": "State and computed values",
                "body": "State is reactive. Computed functions derive values from that state and update when their dependencies change.",
                "code": 'Fyr.createApp("cart", {\n  state: { quantity: 2, price: 12 },\n  computed: {\n    total() { return this.state.quantity * this.state.price; }\n  }\n});',
            },
            {
                "heading": "Keep list updates explicit",
                "body": "For predictable updates, replace arrays when adding, removing, or filtering records.",
                "code": 'this.state.tasks = [\n  ...this.state.tasks,\n  { id: crypto.randomUUID(), title: "Ship Fyr" }\n];',
            },
        ],
    },
    "directives": {
        "title": "Directives",
        "summary": "Directives connect plain HTML to application state, events, conditional UI, and list rendering.",
        "sections": [
            {
                "heading": "Common directives",
                "body": "Use fyr-text for safe text, fyr-model for form state, fyr-click or fyr-on for events, fyr-show or fyr-if for conditional UI, and fyr-for for repeated content.",
                "code": '<input fyr-model="name">\n<p fyr-text="name"></p>\n<button fyr-click="save()">Save</button>\n<p fyr-show="saved">Saved.</p>\n<li fyr-for="task in tasks" fyr-key="task.id" fyr-text="task.title"></li>',
            },
            {
                "heading": "Bindings",
                "body": "Use attribute, class, style, reference, initialization, and transition directives for richer UI behavior.",
                "code": '<img fyr-bind:src="avatarUrl" fyr-bind:alt="name">\n<div fyr-class="{ active: isActive }" fyr-style="{ color: accent }"></div>',
            },
        ],
    },
    "controllers": {
        "title": "Controllers",
        "summary": "Controllers group state, methods, computed values, watchers, and lifecycle work for a Fyr application.",
        "sections": [
            {
                "heading": "Controller definition",
                "body": "Methods run with the controller context, so application state is available as this.state.",
                "code": 'Fyr.createApp("profile", {\n  state: { saved: false },\n  methods: {\n    save() { this.state.saved = true; }\n  },\n  mounted() { console.log("Ready"); }\n});',
            },
        ],
    },
    "components": {
        "title": "Components",
        "summary": "Register components when you need reusable UI definitions; keep the surrounding page API explicit and small.",
        "sections": [
            {
                "heading": "Register a component",
                "body": "Component registration is available in the core API. Build page-level functionality with applications and directives first, then introduce reusable components where they remove real duplication.",
                "code": 'Fyr.component("status-badge", {\n  props: { status: "" },\n  template: "<span fyr-text=\\\"status\\\"></span>"\n});',
            },
        ],
    },
    "http": {
        "title": "HTTP",
        "summary": "Use Fyr's fetch-based HTTP client for browser requests while keeping server authorization on the backend.",
        "sections": [
            {
                "heading": "Request data",
                "body": "Configure a base URL once when your application talks to a shared API.",
                "code": 'Fyr.configure({ baseURL: "/api" });\nconst response = await Fyr.http.get("/projects");\nconsole.log(response.data);',
            },
            {
                "heading": "Send data",
                "body": "Validate data on your server even when the browser validates for usability.",
                "code": 'await Fyr.http.post("/projects", {\n  name: "Fyr public site"\n});',
            },
        ],
    },
    "actions": {
        "title": "Server actions",
        "summary": "Call server-side actions from the browser while keeping secrets, authorization, and sensitive logic on the server.",
        "sections": [
            {
                "heading": "Call an action",
                "body": "Actions are a request convention, not a substitute for server-side authorization and validation.",
                "code": 'const result = await Fyr.action("publishProject", {\n  projectId: "fyr-site"\n});',
            },
        ],
    },
    "routing": {
        "title": "Routing",
        "summary": "The optional router bundle supports hash or history routing, parameters, navigation, and route guards.",
        "sections": [
            {
                "heading": "Create a hash router",
                "body": "Hash routing works on ordinary static hosts. History mode needs a server fallback for unknown client routes.",
                "code": 'import { Router } from "https://cdn.jsdelivr.net/npm/@aldane-dev-create/fyr@0.1.2/dist/fyr-router.esm.js";\n\nconst router = new Router({\n  mode: "hash",\n  routes: [{ path: "/", component: "home" }]\n});',
            },
        ],
    },
    "python": {
        "title": "Browser Python",
        "summary": "Load Pyodide only on pages that need browser-side Python, then run code through Fyr's PyodideLoader.",
        "sections": [
            {
                "heading": "Run Python",
                "body": "The Python bundle is optional. Loading it downloads the Pyodide runtime, so provide a visible loading state.",
                "code": 'import { PyodideLoader } from "https://cdn.jsdelivr.net/npm/@aldane-dev-create/fyr@0.1.2/dist/fyr-python.esm.js";\n\nconst python = new PyodideLoader();\nawait python.load();\nconsole.log(await python.run("2 ** 10"));',
            },
        ],
    },
    "wasm": {
        "title": "WebAssembly",
        "summary": "Use the optional WASM helpers to fetch and compile trusted browser WebAssembly modules.",
        "sections": [
            {
                "heading": "Load a module",
                "body": "The functions exported by a WASM file are decided by that file. Serve WASM with application/wasm.",
                "code": 'import { WasmLoader } from "https://cdn.jsdelivr.net/npm/@aldane-dev-create/fyr@0.1.2/dist/fyr-wasm.esm.js";\n\nconst loader = new WasmLoader({ allowedOrigins: [location.origin] });\nconst module = await loader.load("math", "/wasm/math.wasm");\nconst instance = await WebAssembly.instantiate(module, {});',
            },
        ],
    },
    "plugins": {
        "title": "Plugins",
        "summary": "Plugins provide extension points for directives, components, controllers, and services.",
        "sections": [
            {
                "heading": "Register an extension",
                "body": "Keep plugins focused and document every public behavior they add.",
                "code": 'Fyr.plugin("analytics", context => {\n  context.on("page:view", event => console.log(event));\n});',
            },
        ],
    },
    "api-reference": {
        "title": "API reference",
        "summary": "The Fyr public surface includes application creation, configuration, HTTP, actions, events, notifications, registration, and optional bundles.",
        "sections": [
            {
                "heading": "Core API",
                "body": "Use Fyr.createApp, Fyr.start, Fyr.destroyApp, Fyr.configure, Fyr.http, Fyr.action, Fyr.notify, Fyr.nextTick, Fyr.emit, and Fyr.on from the core bundle.",
                "code": 'Fyr.configure({ debug: true });\nFyr.notify.success("Ready");\nFyr.on("project:created", project => console.log(project));',
            },
            {
                "heading": "Optional bundles",
                "body": "Router, Python, WASM, socket, and UI helpers are separate ES module files so a core-only application stays small.",
                "code": 'fyr-router.esm.js\nfyr-python.esm.js\nfyr-wasm.esm.js\nfyr-socket.esm.js\nfyr-ui.esm.js',
            },
        ],
    },
}

EXAMPLES = {
    "counter": {
        "title": "Counter",
        "summary": "Reactive state, methods, text bindings, and an intentional small UI.",
        "focus": ["Reactive state", "Computed labels", "Event handlers"],
        "code": 'Fyr.createApp("counter", {\n  state: { count: 0 },\n  methods: {\n    increment() { this.state.count += 1; }\n  }\n});',
    },
    "todo": {
        "title": "Todo workspace",
        "summary": "List rendering, form binding, filtering, and immutable updates.",
        "focus": ["fyr-for", "fyr-model", "List updates"],
        "code": '<form fyr-submit="addTask">\n  <input fyr-model="draft">\n</form>\n<li fyr-for="task in tasks" fyr-key="task.id" fyr-text="task.title"></li>',
    },
    "forms": {
        "title": "Forms",
        "summary": "Two-way binding, validation messages, and submit handling.",
        "focus": ["Two-way binding", "Validation", "Accessibility"],
        "code": '<input fyr-model="email" type="email">\n<p fyr-show="errors.email" fyr-text="errors.email"></p>',
    },
    "http": {
        "title": "HTTP dashboard",
        "summary": "Fetch data from an API and represent loading, success, and error states.",
        "focus": ["Fyr.http", "Loading state", "Error handling"],
        "code": 'this.state.loading = true;\ntry {\n  this.state.items = await Fyr.http.get("/api/items");\n} finally {\n  this.state.loading = false;\n}',
    },
    "python": {
        "title": "Browser Python",
        "summary": "Run small Python programs in the browser through PyodideLoader.",
        "focus": ["Lazy runtime", "Python code", "Package loading"],
        "code": 'const python = new PyodideLoader();\nawait python.load();\nconst result = await python.run("sum([1, 2, 3])");',
    },
    "wasm": {
        "title": "Rust + WASM",
        "summary": "Load a WebAssembly binary and call its exported functions.",
        "focus": ["WasmLoader", "Native exports", "Performance work"],
        "code": 'const module = await loader.load("engine", "/engine.wasm");\nconst instance = await WebAssembly.instantiate(module, {});',
    },
    "full-stack": {
        "title": "Mini classroom",
        "summary": "A Flask-backed classroom interface with announcements, assignments, and grading flows.",
        "focus": ["Flask API", "Fyr state", "Responsive dashboard"],
        "code": 'const classroom = await Fyr.http.get("/api/classroom");\nthis.state.assignments = classroom.assignments;',
    },
}

POSTS = {
    "why-fyr": {
        "title": "Why Fyr is CDN-first",
        "date": "July 20, 2026",
        "excerpt": "A small framework should let an idea reach the browser without making a build system the first task.",
        "body": [
            "Fyr starts from the browser. A page can import an exact version, create reactive state, and stay close to the HTML it renders.",
            "That does not mean build tools are forbidden. It means they are optional. Use npm when it helps your project, and use a pinned CDN module when direct delivery is the clearest choice.",
        ],
    },
    "building-fyr": {
        "title": "Building Fyr in the open",
        "date": "July 20, 2026",
        "excerpt": "A student-built framework exploring reactive HTML, browser Python, and WebAssembly.",
        "body": [
            "Fyr is a focused learning project and public framework experiment. Its goal is to make frontend concepts visible: state, bindings, controllers, APIs, and optional browser capabilities.",
            "The project is developed by Aldane Hutchinson alongside studies in Computer Networking & Security at UTech, Jamaica.",
        ],
    },
}


def page_context(**extra):
    return {"site": SITE, "navigation": NAVIGATION, **extra}


@app.route("/assets/<path:filename>")
def assets(filename):
    """Serve public assets locally. Vercel serves public/assets from its CDN."""
    return send_from_directory(ROOT / "public" / "assets", filename)


@app.route("/")
def home():
    return render_template("home.html", **page_context(loader_variant="orbital", page="home"))


@app.route("/docs/")
@app.route("/docs")
def docs_index():
    return render_template(
        "docs.html",
        **page_context(loader_variant="ripple", page="docs", docs=DOCS),
    )


@app.route("/docs/<slug>")
def docs_article(slug):
    article = DOCS.get(slug)
    if not article:
        abort(404)
    return render_template(
        "article.html",
        **page_context(loader_variant="ripple", page="docs", article=article, docs=DOCS),
    )


@app.route("/examples/")
@app.route("/examples")
def examples_index():
    return render_template(
        "examples.html",
        **page_context(loader_variant="constellation", page="examples", examples=EXAMPLES),
    )


@app.route("/examples/<slug>")
def example_detail(slug):
    example = EXAMPLES.get(slug)
    if not example:
        abort(404)
    return render_template(
        "example.html",
        **page_context(loader_variant="constellation", page="examples", example=example),
    )


@app.route("/blog/")
@app.route("/blog")
def blog_index():
    return render_template(
        "blog.html",
        **page_context(loader_variant="ripple", page="blog", posts=POSTS),
    )


@app.route("/blog/<slug>")
def blog_post(slug):
    post = POSTS.get(slug)
    if not post:
        abort(404)
    return render_template(
        "blog_post.html",
        **page_context(loader_variant="ripple", page="blog", post=post),
    )


@app.route("/community")
def community():
    return render_template("community.html", **page_context(loader_variant="constellation", page="community"))


@app.route("/contribute")
def contribute():
    return render_template("contribute.html", **page_context(loader_variant="constellation", page="community"))


@app.route("/about")
def about():
    return render_template("about.html", **page_context(loader_variant="orbital", page="about"))


@app.route("/contact")
def contact():
    return render_template("contact.html", **page_context(loader_variant="ripple", page="contact"))


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "site": SITE["name"], "version": SITE["version"]})


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html", **page_context(loader_variant="constellation", page="not-found")), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
