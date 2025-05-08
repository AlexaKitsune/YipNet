<template>
    <label :class="`AlexiconSwitch-MAIN AlexiconSwitch-checked-${currentVal} AlexiconSwitch-disabled-${disabled}`">
        <input type="checkbox" :disabled="disabled" ref="AlexiconCheckbox" :checked="checked" v-model="currentVal" @input="emitValue" @change="emitValue">
        <div></div>
    </label>
</template>

<script>
export default{
    name: 'AlexiconSwitch',
    props: {
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
            const checkboxChecked = this.$refs.AlexiconCheckbox.checked;
            this.isChecked = checkboxChecked;
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
.AlexiconSwitch-MAIN{
    height: 20px;
    width: 40px;
    background-color: light-dark(v-bind('styles.light.switch.default.bg'), v-bind('styles.dark.switch.default.bg'));
    border-radius: 100vw;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    cursor: pointer;
}

.AlexiconSwitch-MAIN input{
    opacity: 0.3;
    display: none;
}

.AlexiconSwitch-MAIN > div{
    width: 14px;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    background-color: gray;
    position: absolute;
    left: 3px;
    transition: left 0.1s;
    background-color: light-dark(v-bind('styles.light.switch.default.check'), v-bind('styles.dark.switch.default.check'));
}

.AlexiconSwitch-checked-true{
    background-color: light-dark(v-bind('styles.light.switch.checked.bg'), v-bind('styles.dark.switch.checked.bg'));
}

.AlexiconSwitch-checked-true > div{
    left: calc(100% - 14px - 3px);
    background-color: light-dark(v-bind('styles.light.switch.checked.check'), v-bind('styles.dark.switch.checked.check'));
}

.AlexiconSwitch-disabled-true{
    cursor: unset;
}

.AlexiconSwitch-disabled-true > div{
    background-color: light-dark(v-bind('styles.light.switch.disabled.bg'), v-bind('styles.dark.switch.disabled.bg'));
    border: 2px solid light-dark(v-bind('styles.light.switch.disabled.check'), v-bind('styles.dark.switch.disabled.check'));
    width: 10px;
    left: 3px;
}

.AlexiconSwitch-disabled-true.AlexiconSwitch-checked-true{
    background-color: light-dark(v-bind('styles.light.switch.disabled.bg'), v-bind('styles.dark.switch.disabled.bg'));
}

.AlexiconSwitch-disabled-true.AlexiconSwitch-checked-true > div{
    left: calc(100% - 10px - 7px);
}
</style>