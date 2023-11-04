<template>
    <main>

        <div class="media-displayer-main">
            <div ref="masonryCol1">
                <div v-for="(media, index) in masonryOrderedMedia[0]" :key="index" class="media-item">
                    <template v-if="mediaType(media) == 'image'">
                        <img :src="media" :alt="`Image ${index + 0}`"  @click="deployPopUp(0, index, true)"/>
                    </template>
                    <template v-else-if="mediaType(media) == 'video'">
                        <div class="media-displayer-video-container" @click="deployPopUp(0, index, true)">
                            <video oncontextmenu="return false;" :src="media+'#t=1'" controls :alt="`Video ${index + 0}`">
                            Tu navegador no admite el elemento de video.
                            </video>
                        </div>
                    </template>
                </div>
            </div>

            <div ref="masonryCol2">
                <div v-for="(media, index) in masonryOrderedMedia[1]" :key="index" class="media-item">
                    <template v-if="mediaType(media) == 'image'">
                        <img :src="media" :alt="`Image ${index + 1}`"  @click="deployPopUp(1, index, true)"/>
                    </template>
                    <template v-else-if="mediaType(media) == 'video'">
                        <div class="media-displayer-video-container"  @click="deployPopUp(1, index, true)">
                            <video oncontextmenu="return false;" :src="media+'#t=1'" controls :alt="`Video ${index + 1}`">
                            Tu navegador no admite el elemento de video.
                            </video>
                        </div>
                    </template>
                </div>
            </div>

            <div ref="masonryCol3">
                <div v-for="(media, index) in masonryOrderedMedia[2]" :key="index" class="media-item">
                    <template v-if="mediaType(media) == 'image'">
                        <img :src="media" :alt="`Image ${index + 2}`"  @click="deployPopUp(2, index, true)"/>
                    </template>
                    <template v-else-if="mediaType(media) == 'video'">
                        <div class="media-displayer-video-container"  @click="deployPopUp(2, index, true)">
                            <video oncontextmenu="return false;" :src="media+'#t=1'" controls :alt="`Video ${index + 2}`">
                            Tu navegador no admite el elemento de video.
                            </video>
                        </div>
                    </template>
                </div>
            </div>
        </div>
        
        <!-- viewer popup -->
        <div class="media-displayer-popup" ref="mediaDisplayerPopUp">
            <div class="media-displayer-image-container">
                <template v-if="currentMediaType === 'image'">
                    <img :src="currentMedia"/>
                </template>
                <template v-else-if="currentMediaType === 'video'">
                    <video :src="currentMedia" controls>
                    Tu navegador no admite el elemento de video.
                    </video>
                </template>
            </div>

            <div class="media-displayer-carrete">
                <div class="media-displayer-carrete-images">
                    <div v-for="(media, index) in allMedia" :key="index" class="media-displayer-carrete-item">
                        <template v-if="mediaType(media) == 'image'">
                            <img :src="media" :alt="`Image ${index + 2}`"  @click="deployPopUp(2, index, false)"/>
                        </template>
                        <template v-else-if="mediaType(media) == 'video'">
                            <div @click="deployPopUp(0, index, false)">
                                <video oncontextmenu="return false;" :src="media+'#t=1'" controls :alt="`Video ${index + 2}`">
                                Tu navegador no admite el elemento de video.
                                </video>
                            </div>
                        </template>
                    </div>
                </div>
            </div>

            <div @click="closePopUp()" class="media-displayer-close"></div>
        </div>

    </main>
</template>
  
<script>
export default {
    name: 'MediaDisplayer',
    props: {
        ownerId: Number,
        postId: String,
        images: Array,
    },
    data(){
        return{
            allMedia: [],
            masonryOrderedMedia: [[], [], []],
            mediaTypes: {
                "image": ["jpeg", "jpg", "png", "gif", "bmp", "webp", "svg"],
                "video": ["mp4", "webm", "ogg"]
            },
            currentMediaType: "",
            currentMedia: "" 
        }
    },
    methods:{

        mediaType(media_) {
            let result = media_.split(".");
            result = result[result.length - 1].toLowerCase();

            if(media_.includes("image/png"))
                return "image";
            if (this.mediaTypes.image.includes(result)) {
                return "image";
            } else if (this.mediaTypes.video.includes(result)) {
                return "video";
            } else {
                return "unknown"; // Por ejemplo, si no coincide con ningún tipo conocido
            }
        },

        createMasonry(){
            const inputArray =this.allMedia;
            const groupsOfThree = [];
            for (let i = 0; i < inputArray.length; i += 3)
                groupsOfThree.push(inputArray.slice(i, i + 3));

            const resultArrays = [[], [], []];

            for (let i = 0; i < groupsOfThree.length; i++) {
                const group = groupsOfThree[i];
                for (let j = 0; j < group.length; j++)
                    resultArrays[j].push(group[j]);
            }
            this.masonryOrderedMedia = resultArrays;
        },

        deployPopUp(arrayOrigin_, image_, show_){
            console.log(arrayOrigin_, image_, show_);
            if(show_){
                event.preventDefault();
                this.$refs.mediaDisplayerPopUp.style.display = "flex";
                //this.$refs.mediaDisplayerImage.src = this.masonryOrderedMedia[arrayOrigin_][image_];

                this.currentMediaType = this.mediaType(this.masonryOrderedMedia[arrayOrigin_][image_]);
                this.currentMedia = this.masonryOrderedMedia[arrayOrigin_][image_];
            }else{
                this.currentMediaType = this.mediaType(this.allMedia[image_]);
                this.currentMedia = this.allMedia[image_];
                
            }
            console.log(this.currentMedia)
        },

        closePopUp(){
            this.$refs.mediaDisplayerPopUp.style.display = "none";
            this.currentMediaType = "";
            this.currentMedia = "";
        }
    },

    mounted(){
        try {
            this.allMedia = JSON.parse(this.images);
        } catch (error) {
            this.allMedia = [];   
        }

        for (let i = 0; i < this.allMedia.length; i++) {
            this.allMedia[i] = `${this.$ENDPOINT}/static/users/${this.ownerId}/` + this.allMedia[i];
        }

        this.createMasonry();
    }
};
</script>
  
<style scoped>
:root {
  color-scheme: dark;
}

.media-displayer-main {
    width: 100%;
    max-width: 512px;
    display: flex;
    justify-content: space-between;
    margin-top: 2ch;
}

.media-displayer-main > div{
    width: calc(33.3% - 1ch);
}

.media-item {
  margin-bottom: 1.5ch;
}

.media-item img, .media-displayer-video-container video{
  width: 100%;
  border-radius: 1ch;
}

.media-item img:hover, .media-displayer-carrete-item img:hover, .media-displayer-video-container video:hover{
    filter: brightness(0.9);
    cursor: pointer;
    transition: filter 0.2s;
}

.media-displayer-video-container video{
    pointer-events: none;
}

/* PopUp */
.media-displayer-popup{
    position: fixed;
    width: 100%;
    min-height: 100vh;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    background-color: rgba(0, 0, 0, 0.75);
    display: none;
    z-index: 1;
}

.media-displayer-image-container{
    width: 100%;
    height: calc(100vh - 100px - 4ch);
    display: flex;
    align-items: center;
    justify-content: center;
}

.media-displayer-image-container > img, .media-displayer-image-container video{
    max-width: 80%;
    max-height: 80%;
    z-index: 1;
    cursor: crosshair;
}

.media-displayer-carrete{
    height: calc(100px + 2ch);
    width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    /* Estilos para la barra de desplazamiento en navegadores Gecko */
    scrollbar-width: thin;
    scrollbar-color: rgb(145, 145, 145) rgb(50,50,50);
    z-index: 1;
}

.media-displayer-carrete-images{
    min-width: 100%;
    width: fit-content;
    height: inherit;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2ch;
}

.media-displayer-carrete-item{
    width: fit-content;
    height: inherit;
}

.media-displayer-carrete-item img, .media-displayer-carrete-item video{
    height: 100px;
    width: auto;
    margin: 0 1ch;
    border-radius: 1ch;
}

.media-displayer-carrete-item video{
    pointer-events: none;
}

.media-displayer-close{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background-color: transparent;
    z-index: 0;
}

/********************************************************************
* RESPONSIVE
********************************************************************/
@media all and (max-width:780px){

    .media-displayer-main {
        max-width: unset;
    }

}
</style>
  