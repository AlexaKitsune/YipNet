<template>
  <div>
    <div ref="render3D" class="render3D"></div>
  </div>
</template>
  
<script>
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js"; // Importa el cargador de GLTF
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
//import { DirectionalLight } from "three"; 
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
//import { AmbientLight } from 'three';


export default {
  name: "TriDimension",
  props: {
    modelURL: String,
  },
  mounted() {
    this.initThree();
  },
  methods: {

    modelLoader(modelSource_, fn_){
      const fileExtension = modelSource_.split('.').pop().toLowerCase();

      if(fileExtension == 'gltf'){
        let loader = new GLTFLoader();
        loader.load(modelSource_, function (gltf) {
          const model = gltf.scene;
          model.scale.set(0.3, 0.3, 0.3);
          model.position.set(0, 0, 0);
          fn_.scene.add(model);
          fn_.animate();
        }, undefined, function (error) {
          console.error(error);
        });
      } else

      if(fileExtension == 'stl'){
        let loader = new STLLoader();
        loader.load(modelSource_, function ( geometry ) {
            const material = new THREE.MeshPhongMaterial({ specular: 0xffffff, shininess: 30 });
            var mesh = new THREE.Mesh( geometry, material );
            mesh.scale.set(1, 1, 1);
            mesh.position.set( 0, 0, 0);
            fn_.scene.add( mesh );
        } );
      } else

      if(fileExtension == 'obj'){
        let loader = new OBJLoader();
        loader.load(modelSource_, function ( object ){
          const meshToScale = object.children[0]; // Accede al primer objeto dentro del archivo OBJ
          if (meshToScale) {
            meshToScale.scale.set(0.5, 0.5, 0.5); // Aplica la escala al objeto
            fn_.scene.add(object);
          } else {
            console.log('No se encontraron objetos para escalar.');
          }
        },
        function ( xhr ) {
          console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
        },
        function ( error ) {
          console.log( 'An error happened', error );
        });
      }
    },

    initThree(){
      const RENDER3D = this.$refs.render3D;

      const scene = new THREE.Scene();
      scene.background = new THREE.Color( 0x404040 );
      const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
      camera.position.z = 5;

      const renderer = new THREE.WebGLRenderer();
      renderer.setSize( RENDER3D.clientWidth, RENDER3D.clientHeight );
      RENDER3D.appendChild(renderer.domElement);

      const light = new THREE.AmbientLight(0xffffff, 5); // soft white light
      scene.add( light );

      // /test/source/gear_fixed.gltf
      // /spaceship/source/model.gltf
      // /cat/cat.obj
      const modelSource = '/testmodels/cat.obj';
      this.modelLoader(modelSource, {'scene':scene, 'animate':animate});

      const controls = new OrbitControls(camera, renderer.domElement);
      controls.minDistance = 1;
      controls.maxDistance = 100;
      controls.enablePan = false;
      controls.enableDamping = true;

      function animate() {
        requestAnimationFrame( animate );
        controls.update();
        //cube.rotation.x += 0.01;
        //cube.rotation.y += 0.01;
        renderer.render( scene, camera );
      }

      animate();
    }

  },
};
</script>
  
<style scoped>

.render3D{
  width: 100%;
  aspect-ratio: 1/1;
  margin: 2ch 0;
  border-radius: 1ch;
  overflow: hidden;
}

</style>
  