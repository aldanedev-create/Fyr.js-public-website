import { Fyr } from "https://cdn.jsdelivr.net/npm/@aldane-dev-create/fyr@0.1.2/dist/fyr.esm.js";

const loader = document.querySelector(".page-loader");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function closeLoader() {
  window.setTimeout(() => loader?.classList.add("is-done"), reducedMotion ? 100 : 650);
}

// Keep the loading scene decorative. A slow third-party module must never block the page.
window.setTimeout(closeLoader, 1450);

function mountApp(name, options) {
  if (!document.querySelector(`[fyr-app="${name}"]`)) return;
  Fyr.createApp(name, options);
  Fyr.start(name);
}

mountApp("site", {
  state: { menuOpen: false },
  methods: {
    toggleMenu() {
      this.state.menuOpen = !this.state.menuOpen;
    },
  },
});

mountApp("starter-copy", {
  state: { copyLabel: "Copy" },
  methods: {
    async copyStarter() {
      const code = 'import { Fyr } from "@aldane-dev-create/fyr";\n\nFyr.createApp("starter", { state: { count: 0 } });';
      try {
        await navigator.clipboard.writeText(code);
        this.state.copyLabel = "Copied";
      } catch {
        this.state.copyLabel = "Copy unavailable";
      }
      window.setTimeout(() => { this.state.copyLabel = "Copy"; }, 1600);
    },
  },
});

mountApp("counter-demo", {
  state: { count: 0 },
  computed: {
    label() {
      return this.state.count === 0 ? "Press a button to update state." : `The state is now ${this.state.count}.`;
    },
  },
  methods: {
    increment() { this.state.count += 1; },
    decrement() { this.state.count -= 1; },
  },
});

mountApp("example-counter", {
  state: { count: 0 },
  computed: {
    message() { return this.state.count === 0 ? "Ready when you are." : `Counter updated to ${this.state.count}.`; },
  },
  methods: {
    increment() { this.state.count += 1; },
    decrement() { this.state.count -= 1; },
    reset() { this.state.count = 0; },
  },
});

const docsSearch = document.querySelector("#docs-search");
if (docsSearch) {
  window.addEventListener("keydown", (event) => {
    if (event.key === "/" && document.activeElement !== docsSearch) {
      event.preventDefault();
      docsSearch.focus();
    }
  });
  docsSearch.addEventListener("input", () => {
    const term = docsSearch.value.trim().toLowerCase();
    document.querySelectorAll(".doc-card").forEach((card) => {
      card.hidden = term.length > 0 && !card.dataset.search.toLowerCase().includes(term);
    });
  });
}

async function startThreeLoader() {
  if (reducedMotion) {
    closeLoader();
    return;
  }

  const canvas = document.querySelector("#loader-canvas");
  if (!canvas) return;

  try {
    const THREE = await import("https://cdn.jsdelivr.net/npm/three@0.185.1/build/three.module.js");
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    camera.position.z = 6;
    const group = new THREE.Group();
    scene.add(group);
    const variant = document.body.dataset.loaderVariant || "orbital";
    const material = new THREE.MeshBasicMaterial({ color: 0xd8ff5e, wireframe: true, transparent: true, opacity: 0.78 });
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x9b8cff, transparent: true, opacity: 0.65 });

    if (variant === "ripple") {
      [1.05, 1.55, 2.05].forEach((radius, index) => {
        const ring = new THREE.Mesh(new THREE.RingGeometry(radius - 0.025, radius, 64), new THREE.MeshBasicMaterial({ color: index === 1 ? 0x63e7ff : 0xd8ff5e, transparent: true, opacity: 0.68 }));
        ring.userData.speed = 0.004 + index * 0.0016;
        group.add(ring);
      });
    } else if (variant === "constellation") {
      const points = [];
      for (let i = 0; i < 40; i += 1) {
        points.push(new THREE.Vector3((Math.random() - .5) * 4.8, (Math.random() - .5) * 3.1, (Math.random() - .5) * 1.4));
      }
      const pointGeometry = new THREE.BufferGeometry().setFromPoints(points);
      const pointCloud = new THREE.Points(pointGeometry, new THREE.PointsMaterial({ color: 0xd8ff5e, size: 0.045, transparent: true, opacity: 0.9 }));
      group.add(pointCloud);
      const segments = [];
      points.forEach((point, index) => {
        const peer = points[(index + 7) % points.length];
        segments.push(point, peer);
      });
      group.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(segments), lineMaterial));
    } else {
      group.add(new THREE.Mesh(new THREE.IcosahedronGeometry(1.35, 2), material));
      const ring = new THREE.Mesh(new THREE.TorusGeometry(1.95, 0.015, 8, 90), new THREE.MeshBasicMaterial({ color: 0x63e7ff, transparent: true, opacity: 0.75 }));
      ring.rotation.x = 1.1;
      group.add(ring);
      const ringTwo = new THREE.Mesh(new THREE.TorusGeometry(1.7, 0.012, 8, 90), lineMaterial);
      ringTwo.rotation.x = .35;
      group.add(ringTwo);
    }

    function resize() {
      const width = window.innerWidth;
      const height = window.innerHeight;
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.8));
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    }

    let frame;
    function animate(time) {
      group.rotation.y += variant === "constellation" ? 0.0018 : 0.005;
      group.rotation.x = Math.sin(time * 0.00045) * 0.16;
      if (variant === "ripple") {
        group.children.forEach((ring, index) => {
          const scale = 1 + Math.sin(time * ring.userData.speed + index) * 0.09;
          ring.scale.setScalar(scale);
          ring.rotation.z -= .002 + index * .0006;
        });
      }
      renderer.render(scene, camera);
      frame = requestAnimationFrame(animate);
    }

    resize();
    window.addEventListener("resize", resize, { passive: true });
    frame = requestAnimationFrame(animate);
    const finishScene = () => {
      closeLoader();
      window.setTimeout(() => {
        cancelAnimationFrame(frame);
        renderer.dispose();
      }, 1300);
    };

    if (document.readyState === "complete") {
      finishScene();
    } else {
      window.addEventListener("load", finishScene, { once: true });
    }
  } catch (error) {
    console.warn("Three.js loader could not start.", error);
    closeLoader();
  }
}

startThreeLoader();
