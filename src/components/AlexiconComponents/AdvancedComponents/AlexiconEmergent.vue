<template>
    <main class="AlexiconEmergent-MAIN">
        <section>
            <X @click="close()" class="AlexiconEmergent-close"/>
            <div>
                <h1>{{ title }}</h1>
                <slot></slot>
            </div>
        </section>
    </main>
</template>

<script>
import { X } from 'lucide-vue-next';

export default {
    name: 'AlexiconEmergent',
    components: {
        X
    },
    props: {
        title: String,
    },
    methods: {
        close(){
            this.$emit('close', true);
        }
    }
}
</script>

<style scoped>
.AlexiconEmergent-MAIN{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0,0,0,0.5);
    z-index: 5;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.AlexiconEmergent-MAIN > section{
    color: light-dark(black, white);
    background-color: light-dark(#f2f2f2, #2d2d2d);
    position: relative;
    border-radius: 10px;
    width: 75vw;
    height: fit-content;
    max-height: 75vh;
}

.AlexiconEmergent-MAIN > section > div{
    padding: 15px;
}

.AlexiconEmergent-close{
    position: absolute;
    top: 10px;
    right: 10px;
}

.AlexiconEmergent-close:hover{
    scale: 1.1;
    cursor: pointer;
}
</style>