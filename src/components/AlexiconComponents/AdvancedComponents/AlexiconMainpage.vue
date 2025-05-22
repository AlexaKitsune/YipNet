<template>
<Teleport to="body">
    <div class="AlexiconMainpage-MAIN">
        <slot></slot>
    </div>
</Teleport>
</template>

<script>
export default {
    name: 'AlexiconMainpage',
    props:{
        highlightBtnColor: String,
    },
    data(){
        return{

        }
    },
    methods:{
        
    }
}
</script>

<style scoped>
.AlexiconMainpage-MAIN{
    min-width: 100%;
    height: fit-content;
    background-color: light-dark(white, #222222);
    color: light-dark(black, white);
}

.AlexiconMainpage-MAIN:deep(.Alexicon-container){
    display: flex;
    min-height: calc(100vh - 40px);
}

.AlexiconMainpage-MAIN:deep(.Alexicon-main){
    height: fit-content;
    overflow-y: auto;
    width: 1440px;
    max-width: 90%;
    margin: 0 auto;
    padding: 0 1ch;
    max-width: 100vw;
}

.AlexiconMainpage-MAIN:deep(.Alexicon-main .highlighted-btn){
    color: white;
    background-color: v-bind('highlightBtnColor');
}

.AlexiconMainpage-MAIN:deep(.Alexicon-main .highlighted-btn:disabled){
    opacity: 0.5 !important;
    cursor: unset !important;
    filter: grayscale(0.5);
}
</style>