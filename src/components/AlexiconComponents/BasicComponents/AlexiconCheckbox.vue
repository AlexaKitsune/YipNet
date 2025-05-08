<template>
    <label class="AlexiconCheckbox-MAIN" @click="checkIfChecked()">
        <input type="checkbox" :disabled="disabled" ref="AlexiconCheckbox" :checked="checked" v-model="currentVal" @input="emitValue" @change="emitValue">
        <div :class="`AlexiconCheckbox-${ isChecked?'checked':'' }-${disabled?'disabled':''}`"></div>
    </label>
</template>

<script>
export default {
    name: 'AlexiconCheckbox',
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
.AlexiconCheckbox-MAIN{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    aspect-ratio: 1/1;
    background-color: light-dark(v-bind('styles.light.checkbox.default.bg'), v-bind('styles.dark.checkbox.default.bg'));
    cursor: pointer;
}

.AlexiconCheckbox-MAIN input{
    opacity: 0.3;
    display: none;
}

.AlexiconCheckbox-MAIN > div{
    width: calc(100% - 8px);
    aspect-ratio: 1/1;
    clip-path: polygon(100% 0%, 100% 100%, 0% 100%);
    display: none;
}

.AlexiconCheckbox-checked-{
    display: flex !important;
    background-color: light-dark(v-bind('styles.light.checkbox.checked.check'), v-bind('styles.dark.checkbox.checked.check'));
}

.AlexiconCheckbox--disabled{
    display: flex !important;
    background-color: transparent;
    border: 2px solid light-dark(v-bind('styles.light.checkbox.disabled.check'), v-bind('styles.dark.checkbox.disabled.check'));
    clip-path: unset !important;
}

.AlexiconCheckbox-checked-disabled{
    display: flex !important;
    background-color: light-dark(v-bind('styles.light.checkbox.checkedDisabled.check'), v-bind('styles.dark.checkbox.checkedDisabled.check'));
}
</style>