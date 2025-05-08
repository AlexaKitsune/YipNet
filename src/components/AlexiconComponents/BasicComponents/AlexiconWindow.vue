<template>
    <div :class="`AlexiconWindow-MAIN AlexiconWindow-active-${activeWin} AlexiconWindow-title-${title}`" ref="win" tabindex="-1"
        @mousedown="handleWinActive($event), title === false ? startDragging($event) : null"
        @touchstart="handleWinActive($event), title === false ? startDragging($event) : null"
        @mouseup="inArea = true"
        @touchend="inArea = true"
        :style="{ left: position.x + 'px', top: position.y + 'px' }">
        <div class="AlexiconWindow-bar" @mousedown="startDragging" @touchstart="startDragging" v-if="title != false">
            <p>{{ title }}</p>
            <div class="AlexiconWindow-close">+</div>
        </div>
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'AlexiconWindow',
    props:{
        styles: Object,
        startpoint: Array,
        initialPosition: Array,
        title: undefined,
    },
    data() {
        return {
            position: { x: 0, y: 0 }, // Posición inicial
            dragging: false,
            offsetX: 0,
            offsetY: 0,
            activeWin: false,
            inArea: false,
            confirmActivation: false,
        };
    },
    methods: {
        startDragging(event) {
            this.dragging = true;
            this.offsetX = event.clientX - this.position.x;
            this.offsetY = event.clientY - this.position.y;

            const clientX = event.touches ? event.touches[0].clientX : event.clientX;
            const clientY = event.touches ? event.touches[0].clientY : event.clientY;

            this.offsetX = clientX - this.position.x;
            this.offsetY = clientY - this.position.y;

            document.addEventListener("mousemove", this.handleDragging);
            document.addEventListener("mouseup", this.stopDragging);
            document.addEventListener("touchmove", this.handleDragging, { passive: false }); // Evita el scroll
            document.addEventListener("touchend", this.stopDragging);
        },

        handleDragging(event) {
            if (this.dragging) {
                event.preventDefault(); // Bloquea el desplazamiento de la página en móviles

                const clientX = event.touches ? event.touches[0].clientX : event.clientX;
                const clientY = event.touches ? event.touches[0].clientY : event.clientY;

                this.position.x = clientX - this.offsetX;
                this.position.y = clientY - this.offsetY;
            }
        },

        stopDragging() {
            this.dragging = false;
            document.removeEventListener("mousemove", this.handleDragging);
            document.removeEventListener("mouseup", this.stopDragging);
            document.removeEventListener("touchmove", this.handleDragging);
            document.removeEventListener("touchend", this.stopDragging);
        },

        handleWinActive(){
            this.confirmActivation = true;
            this.activeWin = true;
            setTimeout(() => {
                this.confirmActivation = false;
                setTimeout(() => {
                    this.confirmActivation = false;
                }, 100);
            }, 10);
        },

        handleWinInactive(){
            if(!this.confirmActivation){
                this.activeWin = false;
            }
        },
    },
    mounted() {
        if(typeof this.initialPosition == 'undefined'){
            const aleWin = this.$refs.win;
            const aleW = aleWin.offsetWidth;
            const aleH = aleWin.offsetHeight;
            const winW = window.innerWidth;
            const winH = window.innerHeight;
            this.position.x = (winW/2) - (aleW/2);
            this.position.y = (winH/2) - (aleH/2);
        }else{
            this.position.x = this.initialPosition[0];
            this.position.y = this.initialPosition[1];
        }
        document.addEventListener("mousedown", this.handleWinInactive);
        document.addEventListener("touchstart", this.handleWinInactive);
    },
    beforeUnmount() {
        document.removeEventListener("mousedown", this.handleWinInactive);
        document.removeEventListener("touchstart", this.handleWinInactive);
    },
};
</script>

<style scoped>
.AlexiconWindow-MAIN{
    width: fit-content;
    position: absolute;
    left: 100px;
    top: 100px;
    border-radius: 5px;
    overflow: hidden;
    z-index: 999;
    box-shadow: 0 0 1ch rgba(64, 64, 64, 0.5);
    border: 2px solid light-dark(v-bind('styles.light.window.inactive.bar'), v-bind('styles.dark.window.inactive.bar'));
}

.AlexiconWindow-bar{
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    min-height: 1ch;
    cursor: move;
    font-size: 1.5ch;
    background-color: light-dark(v-bind('styles.light.window.inactive.bar'), v-bind('styles.dark.window.inactive.bar'));
}

.AlexiconWindow-bar p{
    margin: 0 0.5ch;
}

.AlexiconWindow-close{
    border-radius: 100vw;
    aspect-ratio: 1/1;
    font-size: 2.5ch;
    width: 1ch;
    height: 1ch;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    rotate: 45deg;
    margin-right: 0.15ch;
    padding-bottom: 0.2ch;
    padding-left: 0.1ch;
    padding-right: 0.1ch;
    color: red;
}

.AlexiconWindow-close:hover{
    background-color: red;
    color: white;
    cursor: pointer;
}

.AlexiconWindow-active-true{
    border: 2px solid light-dark(v-bind('styles.light.window.active.bar'), v-bind('styles.dark.window.active.bar')) !important;
    z-index: 1001;
}

.AlexiconWindow-active-true > .AlexiconWindow-bar{
    background-color: light-dark(v-bind('styles.light.window.active.bar'), v-bind('styles.dark.window.active.bar')) !important;
    color: white;
}

.AlexiconWindow-active-true .AlexiconWindow-close{
    color: white !important;
}

.AlexiconWindow-title-false{
    border: none !important;
}

.AlexiconWindow-title-false *{
    cursor: move;
}
</style>
