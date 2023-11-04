<template>
    <main>
        <div>
            <span>{{ requestedURL }}</span>&nbsp; Not found
        </div>
    </main>
</template>
  
<script>
export default {
    name: "NotFound",
    data() {
        return {
            requestedURL: "",
        };
    },

    methods: {
        getRequestedURL() {
            let text = window.location.href;
            text = text.split("#")[1];
            return text;
        },
    },

    mounted() {
        this.requestedURL = this.getRequestedURL();
        // Agrega un listener para el evento hashchange
        window.addEventListener("hashchange", () => {
            this.requestedURL = this.getRequestedURL();
        });
    },

    // Asegúrate de eliminar el listener cuando el componente se destruye
    beforeUnmount() {
        window.removeEventListener("hashchange", () => {
            this.requestedURL = this.getRequestedURL();
        });
    },
};
</script>
  
<style scoped>
main > div {
  display: flex;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 6.1ch);
  width: 99%;
}

main > div > span {
  color: lightgray;
}
</style>
  