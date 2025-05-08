<template>
    <label class="AlexiconRange-MAIN">
        <div v-if="stepSettings.active" class="AlexiconRange-steps">
            <div v-for="n in calculatedSteps" :key="n" class="AlexiconRange-step"></div>
        </div>
        <input type="range" :disabled="disabled" :step="step" :min="min" :max="max" ref="inputRange" v-model="currentVal" @input="emitValue" @change="emitValue">
        <div v-if="stepSettings.active" class="AlexiconRange-steps">
            <div v-for="n in calculatedSteps" :key="n" class="AlexiconRange-step"></div>
        </div>
    </label>
</template>

<script>
export default {
    name: 'AlexiconRange',
    props:{
        styles: Object,
        disabled: Boolean,
        step: Number,
        min: Number,
        max: Number,
        val: undefined,
    },
    data(){
        return{
            stepSettings: {
                active: false,
                calculatedSteps: 0,
            },
            currentVal: undefined,
        }
    },
    methods: {
        emitValue(){
            this.$emit('get-val', this.currentVal);
        }
    },
    mounted(){
        if(typeof this.step == 'number'){
            this.calculatedSteps = ((this.max - this.min)/this.step +1);
            this.stepSettings.active = true;
        }
        if(this.val){
            this.$refs.inputRange.value = this.val;
            this.currentVal = this.val;
        }
        this.emitValue();
    },
    watch: {
        val(newVal) {
            if (newVal !== undefined) {
                this.$refs.inputRange.value = newVal;
                this.currentVal = newVal;
                this.emitValue();
            }
        }
    },
}
</script>

<style scoped>
.AlexiconRange-MAIN{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 25px;
}

.AlexiconRange-steps{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.AlexiconRange-step{
    width: 2px;
    height: 6px;
    background-color: light-dark(v-bind('styles.light.range.default.step'), v-bind('styles.dark.range.default.step'));
}

.AlexiconRange-MAIN input{
    -webkit-appearance: none;
    appearance: none;
    background: light-dark(v-bind('styles.light.range.default.bg'), v-bind('styles.dark.range.default.bg'));
    height: 5px;
    border-radius: 100vw;
    width: 100%;
    z-index: 0;
}

.AlexiconRange-MAIN input::-webkit-slider-thumb{
    -webkit-appearance: none;
    appearance: none;
    width: 10px;
    height: 25px;
    background: light-dark(v-bind('styles.light.range.default.thumb'), v-bind('styles.dark.range.default.thumb'));
    border: none;
}

.AlexiconRange-MAIN input::-moz-range-thumb {
    width: 10px;
    height: 25px;
    background: light-dark(v-bind('styles.light.range.default.thumb'), v-bind('styles.dark.range.default.thumb'));
    border: none;
}

.AlexiconRange-MAIN input:disabled::-webkit-slider-thumb,
.AlexiconRange-MAIN input:disabled::-moz-range-thumb{
    background: light-dark(v-bind('styles.light.range.disabled.thumb'), v-bind('styles.dark.range.disabled.thumb'));
}
</style>