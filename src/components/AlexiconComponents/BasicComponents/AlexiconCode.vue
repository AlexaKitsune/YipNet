<!--https://highlightjs.org/-->
<template>
    <div class="AlexiconCode-MAIN" ref="code">
        <pre><code v-html="renderedCode"></code></pre>
    </div>
</template>

<script>
const hljs = require('highlight.js');
//import 'highlight.js/styles/base16/atelier-seaside-light.css';
import 'highlight.js/styles/tokyo-night-dark.css';

export default {
    name: 'AlexiconCode',
    props:{
        styles: Object,
        val: undefined,
    },
    data(){
        return{
            currentCode: '',
            renderedCode: '',
        }
    },
    methods:{
        renderHightlight(){
            const highlightedCode = hljs.highlightAuto(this.currentCode).value;
            this.renderedCode = highlightedCode;
        }
    },
    mounted(){
        if(this.val){
            this.currentCode = this.val;
            this.renderHightlight();
        }
    },
    watch: {
        val(newVal) {
            if (newVal !== undefined) {
                this.currentCode = newVal;
                this.renderHightlight();
            }
        }
    },
}
</script>

<style scoped>
.AlexiconCode-MAIN{
    background-color: rgb(26, 27, 38);
    color: rgb(154, 165, 206);
    font-size: 1.5ch;
    padding: 1ch;
}

.AlexiconCode-MAIN pre{
    margin: 0;
    max-width: 100%;
    overflow-y: auto;
}
</style>