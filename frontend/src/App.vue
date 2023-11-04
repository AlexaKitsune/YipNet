<template>
  <YipNet/>
</template>

<script>
import YipNet from './YipNet.vue'
export default {
  name: 'App',
  components: {
    YipNet
  }
}
</script>

<style>
body{
  margin: 0;
  background-color: rgb(32, 33, 36);
}

*{
  scroll-behavior: smooth;
}

#app {
  -moz-osx-font-smoothing: grayscale;
}

/* switch */
.switch{
  position: relative;
  display: flex;
  width: 4.8ch;
  height: 2.5ch;
  border-radius: 100vw;
  overflow: hidden;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;position: absolute;
}

.switch .slider{
  width: 2.4ch;
  height: 2.4ch;
  transform: scale(0.7);
  border-radius: 100vw;
  background-color: white;
  margin-left: 0;
  transition: all 0.2s;
  z-index: 0;
}

.switch input:checked + .slider{
  margin-left: 2.4ch;
  transition: all 0.2s;
}

.switch-bg{
  position: absolute;
  height: 100%;
  width: 100%;
  background-color: gray;
  z-index: 0;
  mix-blend-mode: color-dodge !important;
}

.switch input:checked ~ .switch-bg{
  background-color: rgba(0, 255, 255, 0.75);
}

input[type=text], input[type=password], input[type=email], input[type=date]{
  padding: 0.75ch;
}

.BIG-BUTTON{
  border: none;
  background-color: unset;
  padding:1.4ch 2.4ch;
  cursor: pointer;
  border-radius: 0.5ch;
  transition: all 0.1s;
}

.MAIN-BUTTON{
  color: aqua;
  background-color: rgb(55, 55, 55);
  border: none;
  border-radius: 0.5ch;
} 

.MAIN-BUTTON:hover{
  color: black;
  background-color: aqua;
  transition: all 0.2s;
  cursor: pointer;
}

.SECONDARY-BUTTON{
  color: white;
  background-color: rgb(55, 55, 55);
}

.SECONDARY-BUTTON:hover{
  color: black;
  background-color: lightgray;
  transition: all 0.2s;
}

.MIN-BUTTON{
  border: none;
  color: aqua;
  background-color: transparent;
}

.MIN-BUTTON:hover{
  cursor: pointer;
  color: white;
  transition: all 0.2s;
}
</style>
