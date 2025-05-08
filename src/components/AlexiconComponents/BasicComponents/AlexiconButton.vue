<template>
    <button
        class="AlexiconButton-MAIN"
        :disabled="disabled"
    >
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: 'AlexiconButton',
    props:{
        styles: Object,
        disabled: Boolean,
    }
}
</script>

<style scoped>
.AlexiconButton-MAIN{
    border-radius: 100vw;
    border: none;
    color: light-dark(v-bind('styles.light.button.default.txt'), v-bind('styles.dark.button.default.txt'));
    background-color: light-dark(v-bind('styles.light.button.default.bg'), v-bind('styles.dark.button.default.bg'));
    min-width: 50px;
    padding: 3px calc(1ch + 3px);
}

.AlexiconButton-MAIN:hover{
    cursor: pointer;
}

.AlexiconButton-MAIN:disabled{
    color: light-dark(v-bind('styles.light.button.disabled.txt'), v-bind('styles.dark.button.disabled.txt'));
    background-color: light-dark(v-bind('styles.light.button.disabled.bg'), v-bind('styles.dark.button.disabled.bg'));
    cursor: unset;
}
</style>