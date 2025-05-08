<template>
    <input
        ref="inputText"
        type="text"
        class="AlexiconText-MAIN"
        :placeholder="placeholder"
        :disabled="disabled"
        v-model="currentVal" @input="emitValue" @change="emitValue"
    >
</template>

<script>
export default {
    name: 'AlexiconText',
    props: {
        styles: Object,
        val: undefined,
        placeholder: String,
        disabled: Boolean
    },
    data(){
        return{
            currentVal: undefined,
        }
    },
    methods: {
        emitValue(){
            this.$emit('get-val', this.currentVal);
        }
    },
    mounted(){
        if(this.val){
            this.$refs.inputText.value = this.val;
            this.currentVal = this.val;
        }
        this.emitValue();
    },
    watch: {
        val(newVal) {
            if (newVal !== undefined) {
                this.$refs.inputText.value = newVal;
                this.currentVal = newVal;
                this.emitValue();
            }
        }
    },
}
</script>

<style scoped>
</style>