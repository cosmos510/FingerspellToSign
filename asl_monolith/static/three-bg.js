// Three.js Background Animation
class ThreeBackground {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.particles = null;
        this.mouse = { x: 0, y: 0 };
        this.init();
    }

    init() {
        // Scene
        this.scene = new THREE.Scene();

        // Camera
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.z = 5;

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0x000000, 0);
        
        const container = document.getElementById('three-bg');
        if (container) {
            container.appendChild(this.renderer.domElement);
        }

        // Create particles
        this.createParticles();

        // Event listeners
        window.addEventListener('resize', () => this.onWindowResize());
        document.addEventListener('mousemove', (e) => this.onMouseMove(e));

        // Start animation
        this.animate();
    }

    createParticles() {
        const geometry = new THREE.BufferGeometry();
        const particleCount = 100;
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount * 3; i += 3) {
            positions[i] = (Math.random() - 0.5) * 10;
            positions[i + 1] = (Math.random() - 0.5) * 10;
            positions[i + 2] = (Math.random() - 0.5) * 10;

            // Colors (purple/blue theme)
            colors[i] = 0.4 + Math.random() * 0.4;     // R
            colors[i + 1] = 0.2 + Math.random() * 0.6; // G
            colors[i + 2] = 0.8 + Math.random() * 0.2; // B
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 0.05,
            vertexColors: true,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending
        });

        this.particles = new THREE.Points(geometry, material);
        this.scene.add(this.particles);
    }

    onMouseMove(event) {
        this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        if (this.particles) {
            this.particles.rotation.x += 0.001;
            this.particles.rotation.y += 0.002;
            
            // Mouse interaction
            this.particles.rotation.x += this.mouse.y * 0.001;
            this.particles.rotation.y += this.mouse.x * 0.001;
        }

        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (typeof THREE !== 'undefined') {
        new ThreeBackground();
    }
});