<template>
    <div class="AlexiconMedia-MAIN" @mouseover="mouseOverVideo = true, controlsShowHide()" @mouseleave="mouseOverVideo = false, controlsShowHide()">
        
        <video v-if="type == 'video'"
            :autoplay="autoplay"
            ref="media"
            :loop="loopMode"
            @click="mediaPlayPause(!playing)"
            @timeupdate="updateTimes"
            @loadedmetadata="initializeTimes">
            <source :src="src">
            Your browser does not support the video tag.
        </video>

        <audio v-if="type == 'audio'"
            :autoplay="autoplay"
            ref="media"
            :loop="loopMode"
            @click="mediaPlayPause(!playing)"
            @timeupdate="updateTimes"
            @loadedmetadata="initializeTimes">
            <source :src="src">
            Your browser does not support the audio element.
        </audio> 

        <div class="AlexiconMedia-panel">
            <div class="AlexiconMedia-rendered-cc" v-show="currentCc != null && ccMode" ref="cc">
                <span>{{ currentCc }}</span>
            </div>
            <div class="AlexiconMedia-progress" ref="progress"
                @mousedown="setBarData('startTracking', $event)"
                @mouseup="setBarData('stopTrackingMouseup', $event)"
                @mouseleave="setBarData('stopTrackingMouseleave', $event)"
                @mousemove="setBarData('handleMove', $event)"
                @touchstart="setBarData('startTracking', $event)"
                @touchend="setBarData('stopTrackingMouseup', $event)"
                @touchmove="setBarData('handleMove', $event)"
                @touchcancel="setBarData('stopTrackingMouseleave', $event)">
                <div class="AlexiconMedia-progress-bg">
                    <div class="AlexiconMedia-progress-bar" :style="`width: ${bar.isDragging ? bar.coords.x : progress.toFixed(2)}%;`">
                        <div class="AlexiconMedia-progress-thumb"></div>
                    </div>
                </div>
            </div>
            <div class="AlexiconMedia-controls" ref="controls">
                <div>
                    <button @click="mediaPlayPause(false), seek(-1/framerate)">«</button>
                    <button @click="seek(-10)">◁</button>
                    <button v-if="!playing" @click="mediaPlayPause(true)">▶</button>
                    <button v-if="playing" @click="mediaPlayPause(false)">❚❚</button>
                    <button @click="seek(10)">▷</button>
                    <button @click="mediaPlayPause(false), seek(1/framerate)">»</button>
                </div>
                <div>
                    {{ formatTime(currentTime) }}/{{ formatTime(totalTime) }} (-{{ formatTime(leftTime) }})
                </div>
                <div>
                    <button @click="ccMode = !ccMode, vibrate(50), this.$emit('get-cc', ccMode);" :class="`AlexiconMedia-cc AlexiconMedia-cc-${ccMode}`">CC</button>
                    <button @click="loopMode = !loopMode, vibrate(50), this.$emit('get-loop', loopMode);" :class="`AlexiconMedia-loop AlexiconMedia-loop-${loopMode}`">↻</button>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import srtParser2 from "srt-parser-2";

export default {
    name: 'AlexiconMedia',
    props: {
        styles: Object,
        type: String,
        src: String,
        subtitles: String,
        autoplay: Boolean,
        loop: Boolean,
        framerate: {
            type: Number,
            default: 60,
        },
    },
    data(){
        return{
            playing: false,
            totalTime: undefined,
            currentTime: undefined,
            leftTime: undefined,
            progress: 0,
            bar:{
                coords: {x:0, y:0},
                inArea: false,
                mouseDown: false,
                isDragging: false,
                selected: false,
            },
            loopMode: false,
            ccMode: false,
            parsedSrt: null,
            currentCc: null,
            mouseOverVideo: false,
        }
    },
    methods: {
        vibrate(pattern_){
            this.$parent.vibrate(pattern_);
        },

        mediaPlayPause(mode_){
            if(mode_) this.$refs.media.play(); else this.$refs.media.pause();
            this.playing = mode_;
            this.controlsShowHide();
            this.$emit('get-play-pause', mode_);
            this.vibrate(50);
        },

        controlsShowHide(){
            //console.log("show or hide", this.mouseOverVideo)
            const cc = this.$refs.cc;
            const progress = this.$refs.progress;
            const controls = this.$refs.controls;
            if(this.playing && !this.mouseOverVideo){
                setTimeout(() => {
                    if(this.playing){
                        cc.style.bottom = `5px`;
                        progress.style.bottom = `-25px`;
                        controls.style.bottom = `${0 - 25 - 33}px`;
                    }
                }, 500);
                return;
            }
            if(!this.playing || this.mouseOverVideo){
                cc.style.bottom = `${33 + 25 + 5}px`;
                progress.style.bottom = `33px`;
                controls.style.bottom = `0px`;
            }
        },

        seek(seconds) {
            this.$refs.media.currentTime += seconds;
            this.vibrate(50);
            this.$emit('get-seek', seconds);
        },

        updateTimes() {
            const media = this.$refs.media;
            this.currentTime = this.$refs.media.currentTime.toFixed(2);
            this.leftTime = (this.totalTime - this.currentTime).toFixed(2);
            this.progress = (media.currentTime / media.duration) * 100 || 0;
            if(this.parsedSrt != null){
                this.renderSubtitles();
            }
            this.$emit('get-current-time', this.currentTime);
        },

        initializeTimes() {
            this.totalTime = this.$refs.media.duration.toFixed(2);
            this.updateTimes();
        },

        //progress
        setBarData(mode_, event){
            if (event?.touches) {
                event = event.touches[0];
            }
            if(mode_ == 'startTracking'){
                this.bar.inArea = true;
                this.bar.mouseDown = true;
                this.bar.isDragging = true;
                this.trackPosition(event);
                // Evitar scroll al arrastrar
                document.addEventListener("touchmove", this.preventScroll, { passive: false });
                document.addEventListener("mousemove", this.trackPosition);
                document.addEventListener("touchmove", this.trackPosition, { passive: false });
                return;
            }
            if(mode_ == 'stopTrackingMouseup'){
                this.bar.mouseDown = false;
                this.bar.isDragging = false;
                this.setTimeFromPercentage(this.bar.coords.x);
                // Eliminar eventos cuando se suelte el knob
                document.removeEventListener("mousemove", this.trackPosition);
                document.removeEventListener("touchmove", this.trackPosition);
                document.removeEventListener("touchmove", this.preventScroll);
                return;
            }
            if(mode_ == 'stopTrackingMouseleave'){
                this.bar.inArea = false;
                if(this.bar.inArea || this.bar.mouseDown){
                    this.bar.isDragging = true;
                }else{
                    this.bar.isDragging = false;
                }
                return;
            }
            if(mode_ == 'handleMove'){
                if (this.bar.isDragging) {
                    this.trackPosition(event);
                }
            }
        },

        trackPosition(event) {
            if (event.touches) {
                event = event.touches[0];
            }

            this.bar.selected = true;
            document.addEventListener("mouseup", () => { this.setBarData('stopTrackingMouseup') });
            document.addEventListener("touchend", () => { this.setBarData('stopTrackingTouchend') });

            const rect = this.$refs.progress.getBoundingClientRect();
            const x = ((event.clientX - rect.left) / rect.width) * 100;
            const y = ((event.clientY - rect.top) / rect.height) * 100;
            if(x > 100){
                this.bar.coords.x = 100;
                return;
            }else
            if(x < 0){
                this.bar.coords.x = 0;
                return;
            }
            this.bar.coords = {x:x, y:y};
            //console.log(`X: ${x.toFixed(2)}%, Y: ${y.toFixed(2)}%`);
            this.setTimeFromPercentage(this.bar.coords.x);
        },

        preventScroll(event) {
            event.preventDefault();
        },

        setTimeFromPercentage(percentage) {
            if(!this.bar.selected) return;
            //console.log("Releasing", percentage);
            this.bar.selected = false;
            const media = this.$refs.media;
            const newTime = (percentage / 100) * media.duration;
            media.currentTime = newTime;
            this.progress = percentage;
            this.vibrate(1);
        },

        parseSrt(){
            var parser = new srtParser2();
            var srt_array = parser.fromSrt(this.subtitles);
            this.parsedSrt = srt_array;
        },

        renderSubtitles() {
            const currentTime = parseFloat(this.currentTime); // Convertimos a número
            const subtitles = this.parsedSrt.filter(
                subtitle => currentTime >= subtitle.startSeconds && currentTime <= subtitle.endSeconds
            );

            // Mostrar el texto del subtítulo o limpiar si no hay ninguno
            if (subtitles.length > 0) {
                //console.log(subtitles[0].text)
                this.currentCc = subtitles[0].text; // Muestra el primer subtítulo activo
            } else {
                this.currentCc = null; // Limpia si no hay subtítulos en este tiempo
            }
        },

        formatTime(seconds) {
            if (isNaN(seconds) || seconds < 0) return "00:00:00";
            let h = Math.floor(seconds / 3600);
            let m = Math.floor((seconds % 3600) / 60);
            let s = Math.floor(seconds % 60);
            return [h, m, s]
                .map(unit => unit.toString().padStart(2, "0"))
                .join(":");
        },
    },
    mounted(){
        if(this.autoplay == true){
            this.playing = true;
        }
        if(this.loop == true){
            this.loopMode = true;
        }
        if(this.subtitles != 'undefined' && this.subtitles?.trim().length > 0){
            this.ccMode = true;
            this.parseSrt();
        }
    }
}
</script>

<style scoped>
.AlexiconMedia-MAIN{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}

.AlexiconMedia-panel{
    width: 100%;
    display: flex;
    flex-direction: column;
    height: fit-content;
    position: absolute;
    bottom: 0;
}

.AlexiconMedia-rendered-cc{
    margin: 0 auto;
    left: 0;
    right: 0;
    width: fit-content;
    height: fit-content;
    text-align: center;
    color: white;
    max-width: 90%;
    position: absolute;
    bottom: 5px;
    transition: bottom 0.5s;
}

.AlexiconMedia-rendered-cc span{
    background-color: rgba(0, 0, 0, 0.5);
    padding: 0 5px;
}

.AlexiconMedia-progress, .AlexiconMedia-controls{
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    transition: bottom 0.5s;
}

/* progress */
.AlexiconMedia-progress{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 10px;
    cursor: pointer;
    height: 25px;
    position: absolute;
    bottom: 33px;
    width: calc(100% - 20px);
}

.AlexiconMedia-progress-bg{
    width: calc(100% - 5px);
    height: 5px;
    background-color: v-bind('styles.light.media.bg');
    display: flex;
    align-items: center;
    border-radius: 100vw;
}

.AlexiconMedia-progress-bar{
    background-color: v-bind('styles.light.media.progress');
    height: 100%;
    border-radius: 100vw;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    transition: width 0.1s;
}

.AlexiconMedia-progress-thumb{
    height: 15px;
    aspect-ratio: 1/1 !important;
    background-color: v-bind('styles.light.media.thumb');
    border-radius: 100vw;
    margin-right: -7.5px;
}
/* end progress */

.AlexiconMedia-controls{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: fit-content;
    height: 33px;
    position: absolute;
    bottom: 0;
}

.AlexiconMedia-controls > div{
    display: flex;
    align-items: center;
    margin: 3px 5px;
    margin-bottom: 5px;
}

button{
    color: white;
    background-color: transparent;
    border: none;
    font-size: 15px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 25px;
    aspect-ratio: 1/1;
    padding-bottom: 2px;
    border-radius: 100vw;
}

button:hover{
    cursor: pointer;
    text-shadow: 0 0 5px white;
 
}

.AlexiconMedia-controls > div:nth-child(1) button{
    margin-right: 3px;
}

.AlexiconMedia-controls > div:nth-child(1) button:hover{
    background-color: v-bind('styles.light.media.progress');
}

.AlexiconMedia-controls > div:nth-child(2){
    font-size: 12px;
}

.AlexiconMedia-controls > div:nth-child(3) button:not(.AlexiconMedia-loop){
    font-size: 14px;
    width: fit-content;
    aspect-ratio: unset;
    margin-left: 3px;
}

.AlexiconMedia-cc{
    border: 1px solid white;
    border-radius: 3px;
    height: fit-content;
    font-size: 10px !important;
    margin-right: 2px;
}

.AlexiconMedia-cc-true{
    background-color: white;
    color: v-bind('styles.light.media.progress');
}

.AlexiconMedia-loop{
    margin-left: 3px;
}

.AlexiconMedia-loop-true{
    color: v-bind('styles.light.media.progress');
    background-color: white;
    font-size: 16px;
    padding-bottom: 5px;
}

.AlexiconMedia-cc-false:hover, .AlexiconMedia-loop-false:hover{
    background-color: v-bind('styles.light.media.progress');
    color: white;
    border: 1px solid transparent;
}
</style>