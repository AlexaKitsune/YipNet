<template>
  <main>

    <div class="post-layout" v-if="loadedPostData">

      <section class="post-user-info">
        <div class="post-userimg updater-profile-pic"
          :style="`background-image:url('${
            this.$ENDPOINT + '/static/users/' + loadedPostData?.ownerData?.id +'/'+ loadedPostData?.ownerData?.currentProfilePic || require('../assets/images/default-user.jpg')
          }');`
        ">
          <a v-if="loadedPostData.ownerData" :href="toProfile(loadedPostData.ownerData.id)"></a>
        </div>
        <div>
          <p class="post-username" v-if="loadedPostData.ownerData"><a :href="toProfile(loadedPostData.ownerData.id)">{{ loadedPostData?.ownerData?.name + ' ' + loadedPostData?.ownerData?.surname }}</a></p>
          <p class="post-date"><a :href="'#/post~'+postData.id">{{ postData?.postDate }}</a></p>
        </div>
      </section>

      <section>
        <MarkdownRenderer class="post-text" :postId="loadedPostData.id" :text="loadedPostData?.content || ''"/>
        <MediaDisplayer v-if="loadedPostData.media" class="post-media" :images="loadedPostData.media" :ownerId="loadedPostData.ownerData.id"/>
      </section>

      <CommentLayout :postId="postData.id" class="post-comments"/>

    </div>
  
    <div v-else>
      Loading...
    </div>

  </main>
</template>
  
<script>
import CommentLayout from './CommentLayout.vue';
import MarkdownRenderer from './postViewer/MarkdownRenderer.vue';
import MediaDisplayer from './postViewer/MediaDisplayer.vue';
export default {
  name: 'TestView',
  components: {
    MarkdownRenderer,
    MediaDisplayer,
    CommentLayout
  },
  props:{
    postData: Object
  },
  data(){
    return{
      loadedPostData: {}
    }
  },
  methods:{
    toProfile(id_){
      const profileUrl = window.location.href.split("#")[0];
      return profileUrl + "#/profile~" + id_ ;
    }
  },

  mounted(){
    const data = this.postData;
    this.loadedPostData = {
      "id": data.id,
      "ownerData": {
          "id": data.ownerId,
          "name": data.name,
          "surname": data.surname,
          "currentProfilePic": data.currentProfilePic //== "" ? null : data.ow
      },
      "date": data.postDate,
      "content": data.content,
      "sharedId": 0,
      "media": data.media,
      "apiOrigin": data.apiOrigin,
      "nsfwPost": data.nsfwPost,
      "privatePost": data.privatePost,
    }

    /*console.log(this.loadedPostData);

    console.log("post data:", typeof this.postData);
    setTimeout(() => {
      console.log("post data:", typeof this.postData);
    }, 1000);*/
  }

};
</script>
  

<style scoped>
.post-layout{
  background-color: rgb(52, 53, 56);
  border-radius: 1ch;
  margin: 2ch;
  width: 100%;
  max-width: calc(100vw - 4ch);
  min-width: 512px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 2ch;
}

.post-layout > * {
  width: calc(100% - 4ch);
}

.post-user-info{
  display: flex;
  align-items: center;
  font-family: sans-serif;
  margin: 2ch 0;
}

.post-userimg{
  width: 5ch;
  height: 5ch;
  border-radius: 100vw;
  background-size: cover;
  background-position: center;
  margin-right: 2ch;
}

.post-userimg > a{
  width: 100%;
  height: 100%;
  display: flex;
}

.post-user-info p{
  margin: 0.5ch;
}

.post-username, .post-username a{
  color: aqua;
  text-decoration: none;
}

.post-username a:hover{
  text-decoration: underline;
}

.post-date{
  color: gray;
  font-size: 1.5ch;
}

.post-date > a{
  color: inherit;
  text-decoration: none;
}

.post-date > a:hover{
  text-decoration: underline;
}

.post-text{
  font-family: sans-serif;
}

/********************************************************************
* RESPONSIVE
********************************************************************/
@media all and (max-width:780px){

  .post-layout{
    min-width: unset;
    max-width: unset;
    width: 90vw;
    margin: 2ch 0;
  }

}
</style>