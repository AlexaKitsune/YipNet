<template>
    <label @click.stop="setPicker(true)" class="AlexiconColor-MAIN" v-if="!standalone">
        <!--<input type="color" v-model="selectedColor">-->
        <div class="AlexiconColor-show" :style="`background-color: ${selectedColor};`"></div>
    </label>
    <ColorPicker v-if="pickerActive || fromStandalone" :styles="styles" :selectedColor="selectedColor" :standalone="standalone"/>
</template>

<script>
import ColorPicker from './ColorPicker.vue';

export default {
    name: 'AlexiconColor',
    inheritAttrs: false,
    components: {
        ColorPicker,
    },
    props:{
        styles: Object,
        disabled: Boolean,
        standalone: Boolean,
        val: undefined,
    },
    data(){
        return{
            selectedColor: undefined,
            pickerActive: false,
            fromStandalone: false,
        }
    },
    methods: {
        vibrate(pattern_){
            this.$parent.vibrate(pattern_);
        },
        
        setSelectedColor(color_){
            this.selectedColor = color_;
            this.emitValue();
        },

        setPicker(active_){
            this.pickerActive = active_;
        },

        emitValue(){
            this.$emit('get-val', this.selectedColor);
        }
    },
    mounted(){
        if(this.val == undefined){
            this.selectedColor = '#000000';
        }else{
            this.selectedColor = this.val;
        }
        if(this.standalone){
            this.fromStandalone = true;
        }
        this.emitValue();
    },
    watch: {
        val(newVal) {
            if (newVal !== undefined) {
                this.selectedColor = newVal;
                this.emitValue();
            }
        }
    },
}
</script>

<style scoped>
.AlexiconColor-MAIN{
    width: fit-content;
}

.AlexiconColor-MAIN input[type=color]{
    display: none;
    pointer-events: none;
}

.AlexiconColor-show{
    height: 20px;
    width: 20px;
    border-radius: 0 100vw 100vw 100vw;
    rotate: 45deg;
    margin-top: 4px;
}

.AlexiconColor-show:hover{
    cursor: crosshair;
}
</style>