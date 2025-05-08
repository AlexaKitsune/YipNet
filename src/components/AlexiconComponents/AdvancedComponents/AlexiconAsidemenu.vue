<template>
    <aside class="AlexiconAsideMenu-MAIN" ref="asideMenu">
        <div ref="menu">
              <slot></slot>
        </div>
    </aside>
</template>

<script>
export default {
    name: 'AlexiconAsideMenu',
    props:{
        active: Boolean,
        size: undefined,
    },
    data(){
        return{
            menuActive: false,
        }
    },
    methods:{

        switchedMenu(isActive){
            const size = this.size;
            const asideMenu = this.$refs.asideMenu;
            const menu = this.$refs.menu;
            menu.style.maxWidth = `${size}px`;
            if(isActive){
                menu.style.width = `${size}px`;
                asideMenu.style.boxShadow = "0 0 1ch light-dark(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.75))";
            }else{
                menu.style.width = '0px';
                asideMenu.style.boxShadow = "unset";
            }
        }

    },
    mounted(){
        this.switchedMenu();
    },
    watch: {
        active(newVal) {
            console.log("Prop active cambió:", newVal);
            this.switchedMenu(newVal);
        }
    },
}
</script>

<style scoped>
.AlexiconAsideMenu-MAIN{
    width: fit-content;
    min-width: fit-content;
    min-height: 100%;
    overflow: visible;
    z-index: 1000;
    background-color: light-dark(rgb(242, 242, 242), #2d2d2d);
}

.AlexiconAsideMenu-MAIN > div{
    height: calc(100vh - 40px);
    transition: width 0.2s;
    position: sticky;
    top: 40px;
    overflow: hidden;
}
</style>
