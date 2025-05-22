<template>
    <main class="AlexiconMasonry-MAIN">

        <div class="AlexiconMasonry-col" :style="`width: ${ 100 / colsNum }%;`" v-for="(item, index) in finalArray" :key="index">
            <div v-for="(subItem, subIndex) in item" :key="subIndex">
                <img :src="subItem" v-if="['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(getFormat(subItem))">
                <video v-if="['mp4', 'mov', 'webm'].includes(getFormat(subItem))">
                    <source :src="subItem" :type="`video/${getFormat(subItem)}`">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    </main>
</template>

<script>
export default {
    name: 'AlexiconMasonry',
    props: {
        media: Array,
        colsNum: Number,
    },
    data(){
        return{
            finalArray: [],
        }
    },
    methods: {
        generateArrayColumns(){
            const media = this.media;
            const n = this.colsNum;

            for(let i = 0; i < n; i++){
                this.finalArray.push([]);
            }

            let selector = 0;
            for(let i of media){
                this.finalArray[selector].push(i)
                selector = selector < n - 1 ? selector + 1 : 0;
            }
        },

        getFormat(str_){
            return str_.split(".")[str_.split(".").length-1];
        }
    },
    mounted(){
        this.generateArrayColumns();
    }
}
</script>

<style scoped>
.AlexiconMasonry-MAIN{
    width: 100%;
    display: flex;
}

.AlexiconMasonry-col{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.AlexiconMasonry-col > div{
    width: 100%;
    display: block;
}

.AlexiconMasonry-col > div > img, .AlexiconMasonry-col > div > video{
    display: block;
    width: 100%;
    border-radius: 5px;
    scale: 0.97;
    margin: 0;
}

.AlexiconMasonry-col > div > img:hover, .AlexiconMasonry-col > div > video:hover{
    cursor: pointer;
    filter: brightness(0.8);
    transition: filter 0.2s;
}
</style>