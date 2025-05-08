<template>
    <div class="AlexiconTextarea-MAIN">
        <div v-if="!standalone" class="AlexiconTextarea-switch">
            <AlexiconSwitch :styles="styles" @get-val="(val) => switchTextareaPreview(val)"/>&nbsp;Preview
        </div>
        <textarea
            v-if="!previewActive"
            ref="inputTextarea"
            :placeholder="placeholder"
            :disabled="disabled"
            v-model="currentVal" @input="emitValue" @change="emitValue"
            :style="resize ? 'resize: vertical;' : ''"
            :maxlength="maxlength"
        >
        </textarea>
        <AlexiconMarkdown v-if="previewActive" :val="currentVal" :key="keyUpdater"/>
    </div>
</template>

<script>
import AlexiconMarkdown from './AlexiconMarkdown.vue';
import AlexiconSwitch from './AlexiconSwitch.vue';

export default {
    name: 'AlexiconTextarea',
    components:{
        AlexiconMarkdown,
        AlexiconSwitch,
    },
    props: {
        styles: Object,
        val: undefined,
        placeholder: String,
        disabled: Boolean,
        standalone: Boolean,
        resize: Boolean,
        maxlength: Number,
    },
    data(){
        return{
            currentVal: '',
            keyUpdater: 0,
            previewActive: false,
        }
    },
    methods: {
        emitValue(){
            this.$emit('get-val', this.currentVal);
            
            if(this.keyUpdater == 1000000){
                this.keyUpdater = 0;
            }
            this.keyUpdater++;
        },

        switchTextareaPreview(preview_){
            this.previewActive = preview_;
        }
    },
    mounted(){
        if(this.val){
            this.$refs.inputTextarea.value = this.val;
            this.currentVal = this.val;
        }
        this.emitValue();
    },
    watch: {
        val(newVal) {
            if (newVal !== undefined) {
                this.$refs.inputTextarea.value = newVal;
                this.currentVal = newVal;
                this.emitValue();
            }
        }
    },
}
</script>

<style scoped>
.AlexiconTextarea-MAIN{
    width: 100%;
    height: 100%;
}

.AlexiconTextarea-switch{
    display: flex;
    align-items: center;
    height: 30px;
}

.AlexiconTextarea-MAIN textarea{
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    width: 100%;
    height: calc(100% - 30px);
    border: none;
    border-radius: 10px;
    resize: none;
    font-size: 1.5ch;
    border: 2px solid light-dark(v-bind('styles.light.text.default.border'), v-bind('styles.dark.text.default.border')) !important;
}
</style>