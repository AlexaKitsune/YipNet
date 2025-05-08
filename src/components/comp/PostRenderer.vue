<template>
    <section class="PostRenderer-MAIN">

        <div class="PostRenderer-head">
            <a href=""><img src=""></a>
            <div>
                <p><a>{{ postData.name }} {{postData.surname}}</a></p>
                <p><a>{{ postData.post_date }}</a></p>
            </div>
        </div>

        <AlexiconComponent :type="'markdown'" :val="postData.content"/>

        <div class="PostRenderer-votes">
        </div>

        <div class="PostRenderer-commentbox">
            <AlexiconComponent :type="'textarea'" @get-val="(val) => commentInputs.text = val" :resize="true" :placeholder="'Comment...'"/>
            <div class="PostRenderer-commentbox-images">
                <div>
                    <img v-for="(item, index) in commentInputs.images" :key="index" :src="item.preview">
                </div>
            </div>
            <div class="PostRenderer-commentbox-buttons">
                <div class="lucide-icon"><Upload/><input type="file" multiple @change="setFilesPreview()" ref="comment-files-input" accept="image/*"></div>
                <div class="lucide-icon"><Trash2/></div>
                <button>Comment</button>
            </div> 
        </div>

    </section>

</template>

<script>
import { Upload, Trash2 } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';

export default {
    name: 'PostRenderer',
    components: {
        AlexiconComponent, Upload, Trash2
    },
    props: {
        postData: Object
    },
    data(){
        return{
            commentInputs: {
                text: "",
                images: []
            }
        }
    },
    methods: {
        setFilesPreview(){
            const input = this.$refs["comment-files-input"];
            const imagesArr = Array.from(input.files);
            const filteredImagesArr = imagesArr.map(file => {
                return {
                    file,
                    preview: URL.createObjectURL(file)
                };
            })
            this.commentInputs.images = [...this.commentInputs.images, ...filteredImagesArr];
        }
    }
}
</script>

<style scoped>
/**#2d2d2d */
.PostRenderer-MAIN{
    color: light-dark(black, white);
    background-color: light-dark(#f2f2f2, #2d2d2d);
    border-radius: 10px;
    padding: 2ch;
    margin-bottom: 4ch;
    box-shadow: 0 0 2ch rgba(0, 0, 0, 0.2);
}

.lucide-icon{
    width: 3ch;
    aspect-ratio: 1/1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.lucide-icon:hover{
    scale: 1.05;
    cursor: pointer;
}

/* head */
.PostRenderer-head{
    display: flex;
    align-items: center;
    height: fit-content;
}

.PostRenderer-head > a{
    border: 1px solid red;
    display: flex;
    width: 50px;
    aspect-ratio: 1/1;
    border-radius: 100vw;
}

.PostRenderer-head > div{
    margin-left: 1ch;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.PostRenderer-head > div > p{
    margin: 0;
}

.PostRenderer-head > div > p:first-child{
    margin-bottom: 0.5ch;
}

.PostRenderer-head > div > p:last-child{
    color: gray;
    font-size: 1.5ch;
}

.PostRenderer-head > div > p a{
    text-decoration: none;
}

.PostRenderer-head > div > p a:hover{
    text-decoration: underline;
    cursor: pointer;
}

/* commentbox */
.PostRenderer-commentbox-buttons{
    margin-top: 1ch;
    display: flex;
    align-items: center;
}

.PostRenderer-commentbox-buttons label{
    display: flex;
    align-items: center;
    margin-right: 3ch;
}

.PostRenderer-commentbox-buttons label:deep(label){
    margin-right: 1ch !important;
}

.PostRenderer-commentbox-buttons .lucide-icon{
    margin-right: 3ch;
}

.PostRenderer-commentbox-buttons button{
    margin-left: auto;
}

.PostRenderer-commentbox-buttons .lucide-icon{
    position: relative;
    cursor: pointer;
}

.PostRenderer-commentbox-buttons .lucide-icon input{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

/* commentbox-images */
.PostRenderer-commentbox-images{
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 100%;
    margin-top: 1ch;
}

.PostRenderer-commentbox-images > div{
    width: fit-content;
    max-width: 100%;
    display: flex;
    align-items: center;
    overflow-x: auto;
}

.PostRenderer-commentbox-images > div img{
    max-width: 100px;
    max-height: 100px;
    border-radius: 5px;
    background-color: rgba(128, 128, 128, 0.25);
    margin: 0 5px;
}
</style>