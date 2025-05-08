<template>
    <header class="AlexiconSearchbar-MAIN" :style="`background-color: light-dark(${backgroundColor.light}, ${backgroundColor.dark});`" ref="searchbar">
        <div>
            <div>
                <button @click="switchMenu()" class="Alexicon-icon-btn"><Menu/></button>
                <img :src="src">
            </div>

            <div :class="`AlexiconSearchbar-bar-set AlexiconSearchbar-bar-focused-${searchFocus}`" tabindex="-1" @click="setFocus(true)">
                <button class="Alexicon-icon-btn Alexicon-searchbar-moveleft" v-if="searchFocus"><MoveLeft :color="'black'"/></button>
                <div role="search">
                    <input type="text" ref="search" :placeholder="placeholder" @focus="setFocus(true)" @blur="setFocus(false)">
                    <button class="Alexicon-icon-btn Alexicon-searchbar-search"><Search :size="20" :color="searchFocus ? 'black' : undefined"/></button>
                </div>
            </div>

            <div>
                <slot></slot>
            </div>
        </div>
    </header>
    <div class="AlexiconSearchbar-spacer" ref="observedElement">{{ detections.isVisible }}</div>
</template>

<script>
import { Search, MoveLeft, Menu } from 'lucide-vue-next';

export default {
    name: 'AlexiconSearchbar',
    components:{
        Search, MoveLeft, Menu
    },
    props:{
        styles: Object,
        val: undefined,
        placeholder: String,
        disabled: Boolean,
        src: String,
        bgcolor: Array,
    },
    data(){
        return{
            searchFocus: false,
            backgroundColor: {light:'rgb(242, 242, 242)', dark:'#2d2d2d'},
            detections: {
                isVisible: true,
                interval: undefined,
                scrollDirection: null,
                lastScrollY: 0,
            },
            menuActive: false,
        }
    },
    methods:{
        switchMenu(){
            this.menuActive = !this.menuActive;
            this.$emit('get-switch-menu', this.menuActive);
        },

        setFocus(mode_){
            this.searchFocus = mode_;
            if(mode_){
                this.$refs.search.focus();
            }else{
                this.$refs.search.blur();
            }
        },

        observeElement(){
            const observer = new IntersectionObserver(
                (entries) => {
                    this.detections.isVisible = entries[0].isIntersecting;
                    const visible = this.detections.isVisible;
                    if(!visible){
                        this.detections.interval = setInterval(() => {
                            this.$refs.searchbar.style.marginTop = "-40px";
                        }, 1000);
                    }else{
                        clearInterval(this.detections.interval);
                        this.$refs.searchbar.style.marginTop = 0;
                    }
                },
                { threshold: 0.01 },
            );
            observer.observe(this.$refs.observedElement);
        },

        handleScroll() {
            const currentScrollY = window.scrollY;
            if(currentScrollY > this.detections.lastScrollY) {
                this.detections.scrollDirection = "down"; // Bajando
            }else if(currentScrollY < this.detections.lastScrollY){
                this.detections.scrollDirection = "up"; // Subiendo
            }
            this.detections.lastScrollY = currentScrollY;

            const scrollDir = this.detections.scrollDirection;
            if(scrollDir == "up"){
                clearInterval(this.detections.interval);
                this.$refs.searchbar.style.marginTop = 0;
            }else if(scrollDir == "down" && !this.detections.isVisible){
                clearInterval(this.detections.interval);
                this.detections.interval = setInterval(() => {
                    this.setFocus(false);
                    this.$refs.searchbar.style.marginTop = "-40px";
                }, 1000);
            }
        }
    },
    mounted(){
        if(this.bgcolor){
            this.backgroundColor = {light:this.bgcolor[0], dark:this.bgcolor[1]};
        }
        if(this.$refs.observedElement){
            this.observeElement();
        }
        window.addEventListener("scroll", this.handleScroll);
        this.$emit('get-switch-menu', this.menuActive);
    },
    beforeUnmount(){
        window.removeEventListener("scroll", this.handleScroll);
    },
    watch: {
        bgcolor(newBgcolor){
            if(newBgcolor && newBgcolor.length === 2){
                this.backgroundColor = {light:newBgcolor[0], dark:newBgcolor[1]};
            }
        }
    },
}
</script>

<style scoped>
.AlexiconSearchbar-MAIN{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 1ch;
    width: 100%;
    height: 40px;
    position: fixed;
    z-index: 1001;
    transition: background-color 0.2s;
    box-shadow: 0 0 1ch light-dark(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.75));
    transition: margin-top 0.4s;
}

.AlexiconSearchbar-spacer{
    height: 40px;
}

.AlexiconSearchbar-MAIN > div{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 100%;
}

.AlexiconSearchbar-MAIN > div > div{
    display: flex;
    align-items: center;
}

.AlexiconSearchbar-bar-set{
    display: flex;
    
    flex-direction: row;
    align-items: center;
    background-color: rgba(128, 128, 128, 0.2);
    width: fit-content;
    border-radius: 100vw;
    padding: 0 1ch;
    font-size: 1.5ch;
    transition: background-color 0.1s;
}

.Alexicon-searchbar-moveleft{
    margin-left: -4px;
}

.Alexicon-searchbar-moveleft > *{
    margin-bottom: -3px;
}

.Alexicon-searchbar-search{
    margin-right: -4px;
}

.Alexicon-searchbar-search > *{
    margin-bottom: -3px;
}

.AlexiconSearchbar-bar-set > div{
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
}

.AlexiconSearchbar-MAIN input[type=text]{
    background-color: transparent;
    height: 100%;
    width: calc();
    margin: 0;
}

.AlexiconSearchbar-bar-focused-true{
    background-color: white;
}

.AlexiconSearchbar-bar-focused-true input[type=text]{
    color: black;
    outline: none;
}
</style>