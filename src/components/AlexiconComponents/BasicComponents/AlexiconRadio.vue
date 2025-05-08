<template>
    <label class="AlexiconRadio-MAIN" @click="checkIfChecked()">
        <input type="Radio" :disabled="disabled" ref="AlexiconRadio" :checked="checked" v-model="currentVal" @input="emitValue" @change="emitValue">
        <div :class="`AlexiconRadio-${ isChecked?'checked':'' }-${disabled?'disabled':''}`"></div>
    </label>
</template>

<script>
export default {
    name: 'AlexiconRadio',
    props:{
        styles: Object,
        disabled: Boolean,
        checked: Boolean,
    },
    data(){
        return{
            isChecked: false,
            currentVal: undefined,
        }
    },
    methods:{
        checkIfChecked(){
            const radioChecked = this.$refs.AlexiconRadio.checked;
            this.isChecked = radioChecked;
            this.currentVal = this.isChecked;
        },

        emitValue(){
            this.$emit('get-val', this.currentVal);
        }
    },
    mounted(){
        this.checkIfChecked();
        this.emitValue();
    }
}
</script>

<style scoped>
.AlexiconRadio-MAIN{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    background-color: light-dark(v-bind('styles.light.radio.default.bg'), v-bind('styles.dark.radio.default.bg'));
    cursor: pointer;
}

.AlexiconRadio-MAIN input{
    opacity: 0.3;
    display: none;
}

.AlexiconRadio-MAIN > div{
    width: calc(100% - 9px);
    aspect-ratio: 1/1;
    border-radius: 100vw;
    display: none;
}

.AlexiconRadio-checked-{
    display: flex !important;
    background-color: light-dark(v-bind('styles.light.radio.checked.check'), v-bind('styles.dark.radio.checked.check'));
}

.AlexiconRadio--disabled{
    display: flex !important;
    background-color: transparent;
    border: 2px solid light-dark(v-bind('styles.light.radio.disabled.check'), v-bind('styles.dark.radio.disabled.check'));
    clip-path: unset !important;
}

.AlexiconRadio-checked-disabled{
    display: flex !important;
    background-color: light-dark(v-bind('styles.light.radio.checkedDisabled.check'), v-bind('styles.dark.radio.checkedDisabled.check'));
}
</style>