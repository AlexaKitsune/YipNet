<template>
    <div class="AlexiconMicroKnob-MAIN" :style="disabled ? 'pointer-events:none;' : ''"
        @mousedown="setKnobData('startTracking', $event)"
        @mouseup="setKnobData('stopTrackingMouseup', $event)"
        @mouseleave="setKnobData('stopTrackingMouseleave', $event)"
        @mousemove="setKnobData('handleMove', $event)">
        <div ref="knob" :class="`AlexiconMicroKnob-d-${disabled}`" :style="`rotate: -${knob.degree}deg;`">
            <div></div>
        </div>
    </div>
</template>

<script>
// eslint-disable no-unused-vars
export default {
    name: 'AlexiconMicroKnob',
    props: {
        styles: Object,
        disabled: Boolean,
        step: Number,
        min: Number,
        max: Number,
        val: undefined,
    },
    data(){
        return{
            knob:{
                coords: {x:0, y:0},
                inArea: false,
                mouseDown: false,
                isDragging: false,
                degree: 0,
            },
        }
    },
    methods:{
        setKnobData(mode_, event){
            if(mode_ == 'startTracking'){
                this.knob.inArea = true;
                this.knob.mouseDown = true;
                this.knob.isDragging = true;
                this.trackRotation(event);
                document.addEventListener("mousemove", this.trackRotation);
                return;
            }
            if(mode_ == 'stopTrackingMouseup'){
                this.knob.mouseDown = false;
                this.knob.isDragging = false;
                document.removeEventListener("mouseup", ()=> { this.setKnobData('stopTrackingMouseup') });
                document.removeEventListener("mousemove", this.trackRotation);
                return;
            }
            if(mode_ == 'stopTrackingMouseleave'){
                this.knob.inArea = false;
                if(this.knob.inArea || this.knob.mouseDown){
                    this.knob.isDragging = true;
                }else{
                    this.knob.isDragging = false;
                }
                return;
            }
            if(mode_ == 'handleMove'){
                if (this.knob.isDragging) {
                    this.trackRotation(event);
                }
            }
        },

        trackRotation(event){
            document.addEventListener("mouseup", ()=> { this.setKnobData('stopTrackingMouseup') });

            const rect = this.$refs.knob.getBoundingClientRect();
            const x = ((event.clientX - rect.left) / rect.width) * 100;
            const y = ((event.clientY - rect.top) / rect.height) * 100;

            const centerX = 50;
            const centerY = 50;

            const relX = x - centerX;
            const relY = centerY - y;

            const radians = Math.atan2(relY, relX);
            let degrees = (radians * 180) / Math.PI;

            // Ajustar para que 0 grados esté en la parte superior
            degrees -= 90;
            if (degrees < 0) degrees += 360;

            this.knob.coords = { x: x, y: y };
            this.knob.degree = degrees;

            //console.log(`X: ${x.toFixed(2)}%, Y: ${y.toFixed(2)}%, Degrees: ${degrees.toFixed(2)}`);
            this.$emit('get-val', this.knob.degree);
        },
    },
    mounted(){
        if(this.val){
            this.knob.degree = this.val;
        }
        this.$emit('get-val', this.knob.degree);
    },
    watch: {
        val(newVal) {
            if (newVal !== undefined) {
                this.knob.degree = newVal;
                this.currentVal = newVal;
                this.$emit('get-val', this.knob.degree);
            }
        }
    },
}
</script>

<style scoped>
.AlexiconMicroKnob-MAIN{
}

.AlexiconMicroKnob-MAIN > div{
    width: 100%;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    background-color: light-dark(v-bind('styles.light.knob.default.bg'), v-bind('styles.dark.knob.default.bg'));
    display: flex;
    flex-direction: column;
    align-items: center;
}

.AlexiconMicroKnob-MAIN > div > div{
    width: 2px;
    height: 33%;
    background: light-dark( v-bind('styles.light.knob.default.thumb'), v-bind('styles.dark.knob.default.thumb'));
    border-radius: 100vw;
    margin-top: 0px;
}

.AlexiconMicroKnob-d-true > div{
    background: light-dark(v-bind('styles.light.knob.disabled.thumb'), v-bind('styles.dark.knob.disabled.thumb')) !important;
}
</style>