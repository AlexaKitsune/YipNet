<template>
    <div :class="`Alexicon-ColorPicker-MAIN Alexicon-ColorPicker-standalone-${standalone}`">

        <div>
            <div class="Alexicon-color-reflex">
                <div :style="`background-color: ${colorFormats.hex};`">&nbsp;</div>
                <p>{{ colorFormats.hex }}</p>
            </div>

            <div>
                <div class="Alexicon-color-circle"
                    @mousedown="setCircleData('startTracking', $event)"
                    @mouseup="setCircleData('stopTrackingMouseup', $event)"
                    @mouseleave="setCircleData('stopTrackingMouseleave', $event)"
                    @mousemove="setCircleData('handleMove', $event)"
                    @touchstart="setCircleData('startTracking', $event)"
                    @touchend="setCircleData('stopTrackingMouseup', $event)"
                    @touchmove="setCircleData('handleMove', $event)"
                    @touchcancel="setCircleData('stopTrackingMouseleave', $event)">
                    <div></div>
                    <div ref="wheel" :style="`rotate: -${circle.degree}deg;`"><div></div></div>
                </div>
                <div class="Alexicon-color-square"
                    ref="square"
                    @mousedown="setSquareData('startTracking', $event)"
                    @mouseup="setSquareData('stopTrackingMouseup', $event)"
                    @mouseleave="setSquareData('stopTrackingMouseleave', $event)"
                    @mousemove="setSquareData('handleMove', $event)"
                    @touchstart="setSquareData('startTracking', $event)"
                    @touchend="setSquareData('stopTrackingMouseup', $event)"
                    @touchmove="setSquareData('handleMove', $event)"
                    @touchcancel="setSquareData('stopTrackingMouseleave', $event)">
                    <div :style="`left: ${square.coords.x}%; top: ${square.coords.y}%;`"></div>
                </div>
            </div>

            <div class="Alexicon-hsl">
                <label>H <input type="number" v-model="colorFormats.hsl.h" @input="autoConvert('hsl')" min="0" max="360"></label>
                <label>S <input type="number" v-model="colorFormats.hsl.s" @input="autoConvert('hsl')" min="0" max="100"></label>
                <label>L <input type="number" v-model="colorFormats.hsl.l" @input="autoConvert('hsl')" min="0" max="100"></label>
            </div>
            <div class="Alexicon-rgb">
                <label>R <input type="number" v-model="colorFormats.rgb.r" @input="autoConvert('rgb')" min="0" max="255"></label>
                <label>G <input type="number" v-model="colorFormats.rgb.g" @input="autoConvert('rgb')" min="0" max="255"></label>
                <label>B <input type="number" v-model="colorFormats.rgb.b" @input="autoConvert('rgb')" min="0" max="255"></label>
            </div>
            <div class="Alexicon-hex">
                <label>HEX <input type="text" v-model="colorFormats.hex" @input="autoConvert('hex')"></label>
            </div>

            <button @click="setPicker(false)" v-if="!standalone">OK</button>
        </div>

    </div>
</template>

<script>
export default {
    name: 'ColorPicker',
    props: {
        styles: Object,
        selectedColor: String,
        standalone: Boolean,
    },
    data(){
        return{
            circle:{
                coords: {x:0, y:0},
                inArea: false,
                mouseDown: false,
                isDragging: false,
                degree: 0,
            },
            square:{
                coords: {x:0, y:0},
                inArea: false,
                mouseDown: false,
                isDragging: false,
                sat: 0,
                lum: 0,
            },
            colorFormats: {
                hsl: { h: 0, s: 0, l: 0 },
                rgb: { r: 0, g: 0, b: 0 },
                hex: "#000000",
            },
        }
    },
    methods: {
        vibrate(pattern_){
            this.$parent.vibrate(pattern_);
        },
        
        setPicker(active_){
            this.$parent.setPicker(active_);
        },

        //circle
        setCircleData(mode_, event){
            if (event?.touches) {
                event = event.touches[0];
            }
            if(mode_ == 'startTracking'){
                this.circle.inArea = true;
                this.circle.mouseDown = true;
                this.circle.isDragging = true;
                this.trackRotation(event);
                // Evitar scroll al arrastrar
                document.addEventListener("touchmove", this.preventScroll, { passive: false });
                document.addEventListener("mousemove", this.trackRotation);
                document.addEventListener("touchmove", this.trackRotation, { passive: false });
                return;
            }
            if(mode_ == 'stopTrackingMouseup'){
                this.circle.mouseDown = false;
                this.circle.isDragging = false;
                // Eliminar eventos cuando se suelte el knob
                document.removeEventListener("mousemove", this.trackRotation);
                document.removeEventListener("touchmove", this.trackRotation);
                document.removeEventListener("touchmove", this.preventScroll);
                return;
            }
            if(mode_ == 'stopTrackingMouseleave'){
                this.circle.inArea = false;
                if(this.circle.inArea || this.circle.mouseDown){
                    this.circle.isDragging = true;
                }else{
                    this.circle.isDragging = false;
                }
                return;
            }
            if(mode_ == 'handleMove'){
                if (this.circle.isDragging) {
                    this.trackRotation(event);
                }
            }
        },

        trackRotation(event){
            if (event.touches) {
                event = event.touches[0];
            }

            document.addEventListener("mouseup", ()=> { this.setCircleData('stopTrackingMouseup') });

            const rect = this.$refs.wheel.getBoundingClientRect();
            const x = ((event.clientX - rect.left) / rect.width) * 100;
            const y = ((event.clientY - rect.top) / rect.height) * 100;

            const centerX = 50;
            const centerY = 50;

            const relX = x - centerX;
            const relY = centerY - y;

            const radians = Math.atan2(relY, relX);
            const degrees = (radians * 180) / Math.PI;

            const normalizedDegrees = (degrees + 360) % 360;

            this.circle.coords = {x: x, y: y};
            this.circle.degree = normalizedDegrees;

            //console.log(`X: ${x.toFixed(2)}%, Y: ${y.toFixed(2)}%, Degrees: ${normalizedDegrees.toFixed(2)}`);

            this.colorFormats.hsl.h = parseInt(this.circle.degree);
            this.autoConvert('hsl');
            this.vibrate(1);
        },

        //square
        setSquareData(mode_, event){
            if (event?.touches) {
                event = event.touches[0];
            }
            if(mode_ == 'startTracking'){
                this.square.inArea = true;
                this.square.mouseDown = true;
                this.square.isDragging = true;
                // Evitar scroll al arrastrar
                document.addEventListener("touchmove", this.preventScroll, { passive: false });
                document.addEventListener("mousemove", this.trackPosition);
                document.addEventListener("touchmove", this.trackPosition, { passive: false });
                return;
            }
            if(mode_ == 'stopTrackingMouseup'){
                this.square.mouseDown = false;
                this.square.isDragging = false;
                // Eliminar eventos cuando se suelte el knob
                document.removeEventListener("mousemove", this.trackPosition);
                document.removeEventListener("touchmove", this.trackPosition);
                document.removeEventListener("touchmove", this.preventScroll);
                return;
            }
            if(mode_ == 'stopTrackingMouseleave'){
                this.square.inArea = false;
                if(this.square.inArea || this.square.mouseDown){
                    this.square.isDragging = true;
                }else{
                    this.square.isDragging = false;
                }
                return;
            }
            if(mode_ == 'handleMove'){
                if (this.square.isDragging) {
                    this.trackPosition(event);
                }
            }
        },

        trackPosition(event) {
            if (event.touches) {
                event = event.touches[0];
            }
            
            document.addEventListener("mouseup", ()=> { this.setSquareData('stopTrackingMouseup') });

            const rect = this.$refs.square.getBoundingClientRect();
            let x = ((event.clientX - rect.left) / rect.width) * 100;
            let y = ((event.clientY - rect.top) / rect.height) * 100;
  
            if(x > 100) { x = 100; this.vibrate(1); }
            if(x < 0) { x = 0; this.vibrate(1); }
            if(y > 100) { y = 100; this.vibrate(1); }
            if(y < 0) { y = 0; this.vibrate(1); }

            this.square.coords = {x:x, y:y};
            this.square.sat = x;
            this.square.lum = 100-y;
            this.colorFormats.hsl.s = this.square.sat.toFixed(2);
            this.colorFormats.hsl.l = this.square.lum.toFixed(2);
            this.autoConvert('hsl');
            //console.log(`X: ${x.toFixed(2)}%, Y: ${y.toFixed(2)}%`);
        },

        preventScroll(event) {
            event.preventDefault();
        },

        //color conversion
        hslToRgb(h, s, l) {
            s /= 100;
            l /= 100;

            const c = (1 - Math.abs(2 * l - 1)) * s;
            const x = c * (1 - Math.abs((h / 60) % 2 - 1));
            const m = l - c / 2;
            let r = 0, g = 0, b = 0;

            if (h >= 0 && h < 60) {
                r = c; g = x; b = 0;
            } else if (h >= 60 && h < 120) {
                r = x; g = c; b = 0;
            } else if (h >= 120 && h < 180) {
                r = 0; g = c; b = x;
            } else if (h >= 180 && h < 240) {
                r = 0; g = x; b = c;
            } else if (h >= 240 && h < 300) {
                r = x; g = 0; b = c;
            } else if (h >= 300 && h < 360) {
                r = c; g = 0; b = x;
            }

            r = Math.round((r + m) * 255);
            g = Math.round((g + m) * 255);
            b = Math.round((b + m) * 255);
            return { r, g, b };
        },

        rgbToHsl(r, g, b) {
            r /= 255;
            g /= 255;
            b /= 255;

            const max = Math.max(r, g, b);
            const min = Math.min(r, g, b);
            const delta = max - min;

            let h = 0,
                s = 0,
                l = (max + min) / 2;

            if (delta !== 0) {
                s = delta / (1 - Math.abs(2 * l - 1));
                switch (max) {
                case r:
                    h = ((g - b) / delta + (g < b ? 6 : 0)) * 60;
                    break;
                case g:
                    h = ((b - r) / delta + 2) * 60;
                    break;
                case b:
                    h = ((r - g) / delta + 4) * 60;
                    break;
                }
            }

            h = Math.round(h);
            s = Math.round(s * 100);
            l = Math.round(l * 100);
            return { h, s, l };
        },

        rgbToHex(r, g, b) {
            const toHex = (v) => v.toString(16).padStart(2, "0");
            return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
        },

        hexToRgb(hex) {
            console.log("hex", hex)
            const parsedHex = hex.replace("#", "");
            console.log("parsedHex", parsedHex);
            const bigint = parseInt(parsedHex, 16);
            const r = (bigint >> 16) & 255;
            const g = (bigint >> 8) & 255;
            const b = bigint & 255;
            return { r, g, b };
        },

        autoConvert(from_){
            if(from_ == 'hsl'){
                const h = this.colorFormats.hsl.h;
                const s = this.colorFormats.hsl.s;
                const l = this.colorFormats.hsl.l;
                this.colorFormats.rgb = this.hslToRgb(h, s, l);
                const hslrgb = this.hslToRgb(h, s, l);
                this.colorFormats.hex = this.rgbToHex(hslrgb.r, hslrgb.g, hslrgb.b);
                this.circle.degree = h;
            }else
            if(from_ == 'rgb'){
                const r = this.colorFormats.rgb.r;
                const g = this.colorFormats.rgb.g;
                const b = this.colorFormats.rgb.b;
                this.colorFormats.hsl = this.rgbToHsl(r, g, b);
                this.colorFormats.hex = this.rgbToHex(r, g, b);
                this.circle.degree = this.colorFormats.hsl.h;
            }else
            if(from_ == 'hex'){
                const hexrgb = this.hexToRgb(this.colorFormats.hex);
                this.colorFormats.hsl = this.rgbToHsl(hexrgb.r, hexrgb.g, hexrgb.b);
                this.colorFormats.rgb = this.hexToRgb(this.colorFormats.hex);
                this.circle.degree = this.colorFormats.hsl.h;
            }
            this.$parent.setSelectedColor(this.colorFormats.hex);
            this.renderBg();
        },
        
        renderBg(){
            const square = this.$refs.square;
            const h = this.colorFormats.hsl.h;
            //const s = this.colorFormats.hsl.s;
            //const l = this.colorFormats.hsl.l; 

            square.style.background = `
                linear-gradient(0deg, black, transparent, white),
                linear-gradient(90deg, hsl(${h} 0 50), hsl(${h} 100 50))
            `;
        }

    },

    mounted(){
        this.colorFormats.hex = this.selectedColor;
        console.log("mounted colorformats", this.colorFormats.hex);
        this.autoConvert('hex');
    }
}
</script>

<style scoped>
.Alexicon-ColorPicker-MAIN{
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    z-index: 3;
}

.Alexicon-ColorPicker-standalone-true{
    width: fit-content;
    height: fit-content;
    position: relative;
    background-color: transparent;
    z-index: unset;
}

.Alexicon-ColorPicker-MAIN > div{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: light-dark(v-bind('styles.light.color.bg'), v-bind('styles.dark.color.bg'));
    border-radius: 10px;
    padding: 10px;
}

.Alexicon-ColorPicker-standalone-true > div{
    width: fit-content;
    height: fit-content;
    background-color: transparent;
}

.Alexicon-ColorPicker-MAIN > div > div:nth-child(2){
    width: 150px;
    aspect-ratio: 1/1;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 5px;
}

.Alexicon-color-reflex{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin-bottom: 10px;
}

.Alexicon-color-reflex > *{
    margin: 0;
    min-width: 10ch;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

/* color selectors */
.Alexicon-color-circle, .Alexicon-color-square{
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.Alexicon-color-circle{
    z-index: 1;
    border-radius: 100vw;
    background: conic-gradient(from 110deg, red, magenta, blue, cyan, green, yellow, orange, red);
}

.Alexicon-color-circle > div:nth-child(1){
    border-radius: 100vw;
    background-color: light-dark(v-bind('styles.light.color.bg'), v-bind('styles.dark.color.bg'));
    width: 75%;
    aspect-ratio: 1/1;
    position: absolute;
    z-index: 2;
}

.Alexicon-color-circle > div:nth-child(2){
    width: 100%;
    aspect-ratio: 1/1;
    position: absolute;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    cursor:move;
}

.Alexicon-color-circle > div:nth-child(2) > div{
    height: 5px;
    min-width: 5px;
    width: 9%;
    margin-right: 1%;
    backdrop-filter: invert(100%);
    border-radius: 100vw;
    border: 2px solid v-bind('styles.light.color.border');
}

.Alexicon-color-square{
    z-index: 2;
    width: 52%;
    height: 52%;
    aspect-ratio: 1/1;
    position: relative;
    cursor: crosshair;
}

.Alexicon-color-square > div:nth-child(1){
    width: 10px;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    border: 2px solid v-bind('styles.light.color.border');
    position: absolute;
    transform-origin: center;
    transform: translateX(-5px) translateY(-5px);
}
/* end color selectors */

.Alexicon-hsl, .Alexicon-rgb, .Alexicon-hex{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 5px 0;
}

.Alexicon-hsl label, .Alexicon-rgb label, .Alexicon-hex label{
    width: 33.3%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: 10px;
}

.Alexicon-hsl > label:nth-child(1),
.Alexicon-rgb > label:nth-child(1),
.Alexicon-hex > label:nth-child(1){
    margin: 0;
}

.Alexicon-hsl input, .Alexicon-rgb input, .Alexicon-hex input{
    width: 8ch;
    margin-left: 10px;
}

.Alexicon-hex{
    margin-bottom: 10px;
}

/* button */
button{
    border-radius: 100vw;
    border: none;
    color: v-bind('styles.light.button.default.txt');
    background-color: v-bind('styles.light.button.default.bg');
    padding: 3px;
    min-width: 50px;
    width: 100%;
}

button:hover{
    cursor: pointer;
}

button:disabled{
    color: v-bind('styles.light.button.disabled.txt');
    background-color: v-bind('styles.light.button.disabled.bg');
    cursor: unset;
}
</style>