<template>
    <div ref="container" class="model-viewer">
        <div v-if="loading" class="model-message">
            Loading 3D model...
        </div>

        <div v-if="errorMessage" class="model-message text-red-300">
            {{ errorMessage }}
        </div>
    </div>
</template>

<script>
import * as THREE from 'three'
import { markRaw } from 'vue'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js'

export default {
    name: 'AlexiconModelViewer',

    props: {
        src: {
            type: String,
            required: true
        },

        extension: {
            type: String,
            required: true
        }
    },

    data() {
        return {
            renderer: null,
            scene: null,
            camera: null,
            controls: null,
            animationId: null,
            loading: false,
            errorMessage: ''
        }
    },

    methods: {
        async init() {
            this.loading = true
            this.errorMessage = ''

            try {
                const el = this.$refs.container
                const width = el.clientWidth || 640
                const height = 420

                this.scene = markRaw(new THREE.Scene())
                this.scene.background = new THREE.Color(0x111111)

                this.camera = markRaw(new THREE.PerspectiveCamera(45, width / height, 0.1, 10000))
                this.camera.position.set(2.5, 2.5, 2.5)

                this.renderer = markRaw(new THREE.WebGLRenderer({ antialias: true }))
                this.renderer.setSize(width, height)
                this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))
                el.appendChild(this.renderer.domElement)

                const ambient = new THREE.AmbientLight(0xffffff, 0.8)
                this.scene.add(ambient)

                const directional = new THREE.DirectionalLight(0xffffff, 1)
                directional.position.set(5, 8, 5)
                this.scene.add(directional)

                const grid = new THREE.GridHelper(10, 10)
                this.scene.add(grid)

                this.controls = markRaw(new OrbitControls(this.camera, this.renderer.domElement))
                this.controls.enableDamping = true

                const object = markRaw(await this.loadModel())
                this.centerObject(object)
                this.scene.add(object)

                window.addEventListener('resize', this.resize)
                this.animate()
            } catch (error) {
                console.error(error)
                this.errorMessage = 'Could not load 3D model.'
            } finally {
                this.loading = false
            }
        },

        async loadModel() {
            if (['glb', 'gltf'].includes(this.extension)) {
                const loader = new GLTFLoader()
                const result = await loader.loadAsync(this.src)
                return result.scene
            }

            if (this.extension === 'obj') {
                const loader = new OBJLoader()
                return loader.loadAsync(this.src)
            }

            if (this.extension === 'stl') {
                const loader = new STLLoader()
                const geometry = await loader.loadAsync(this.src)

                const material = new THREE.MeshStandardMaterial({
                    color: 0xcccccc,
                    roughness: 0.55,
                    metalness: 0.1
                })

                return new THREE.Mesh(geometry, material)
            }

            throw new Error('Unsupported model format.')
        },

        centerObject(object) {
            const box = new THREE.Box3().setFromObject(object)
            const size = box.getSize(new THREE.Vector3())
            const center = box.getCenter(new THREE.Vector3())

            object.position.sub(center)

            const maxDim = Math.max(size.x, size.y, size.z) || 1
            const distance = maxDim * 2.2

            this.camera.position.set(distance, distance * 0.75, distance)
            this.camera.near = maxDim / 100
            this.camera.far = maxDim * 100
            this.camera.updateProjectionMatrix()

            this.controls.target.set(0, 0, 0)
            this.controls.update()
        },

        resize() {
            const el = this.$refs.container
            if (!el || !this.renderer || !this.camera) return

            const width = el.clientWidth || 640
            const height = 420

            this.camera.aspect = width / height
            this.camera.updateProjectionMatrix()
            this.renderer.setSize(width, height)
        },

        animate() {
            this.animationId = requestAnimationFrame(this.animate)
            this.controls?.update()
            this.renderer?.render(this.scene, this.camera)
        },

        disposeObject(object) {
            if (!object) return

            object.traverse?.(child => {
                if (child.geometry) child.geometry.dispose()

                if (child.material) {
                    if (Array.isArray(child.material)) {
                        child.material.forEach(material => material.dispose())
                    } else {
                        child.material.dispose()
                    }
                }
            })
        },

        cleanup() {
            cancelAnimationFrame(this.animationId)
            window.removeEventListener('resize', this.resize)

            if (this.scene) {
                this.scene.children.forEach(child => this.disposeObject(child))
            }

            this.controls?.dispose()
            this.renderer?.dispose()

            if (this.renderer?.domElement?.parentNode) {
                this.renderer.domElement.parentNode.removeChild(this.renderer.domElement)
            }
        }
    },

    mounted() {
        this.init()
    },

    beforeUnmount() {
        this.cleanup()
    }
}
</script>

<style scoped lang="stylus">
.model-viewer
    position relative
    width 100%
    min-height 420px
    overflow hidden
    border-radius 8px
    background #111

.model-viewer :deep(canvas)
    display block
    width 100% !important
    height 420px !important

.model-message
    position absolute
    inset 0
    display flex
    align-items center
    justify-content center
    z-index 1
    background rgba(0, 0, 0, 0.35)
    font-size 0.9rem
    opacity 0.8
</style>