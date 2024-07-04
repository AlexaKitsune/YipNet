<template>
  <main>

    <div class="post-layout" v-if="loadedPostData">

		<section class="post-user-info">
			<div class="post-userimg updater-profile-pic"
				:style="`background-image:url('${
					loadedPostData?.ownerData?.currentProfilePic == ''
					? require('../assets/images/default-user.jpg')
					: this.$ENDPOINT + '/static/users/' + loadedPostData?.ownerData?.id +'/'+ loadedPostData?.ownerData?.currentProfilePic 
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
			<MarkdownRenderer class="post-text ts" :postId="loadedPostData?.id?.toString()" :text="loadedPostData?.content || ''"/>
			<MediaDisplayer v-if="loadedPostData.media" class="post-media" :images="loadedPostData.media" :ownerId="loadedPostData.ownerData.id"/>
		</section>

		<!--Shared post data here-->
		<section v-if="loadedPostData.shareId != 0" class="shared">
			<div>
			<a :href="toPost(loadedSharedPostData.id)" style="text-decoration: none !important;">
				<div v-if="loadedSharedPostData">
					<div class="post-user-info post-user-info-shared">
						<div class="post-userimg updater-profile-pic"
							:style="`background-image:url('${
								this.$ENDPOINT + '/static/users/' + loadedSharedPostData.ownerId +'/'+ loadedSharedPostData.currentProfilePic || require('../assets/images/default-user.jpg')
							}');`
						">
						</div>
						<div>
							<p class="post-username">{{ loadedSharedPostData.name + ' ' + loadedSharedPostData.surname }}</p>
							<p class="post-date">{{ postData?.postDate }}</p>
						</div>
					</div>
					<section>
						<MarkdownRenderer class="post-text" :postId="loadedSharedPostData.id" :text="loadedSharedPostData.content || ''"/>
						<MediaDisplayer v-if="loadedSharedPostData.media" class="post-media" :images="loadedSharedPostData.media" :ownerId="loadedSharedPostData.ownerId"/>
					</section>
				</div>
				<div v-else>
					Loading...
				</div>
			</a>
			</div>
		</section>
		<!--End shared post-->

      <CommentLayout
		:postId="postData.id.toString()"
		:numOfComments="postData.commentCount"
		:shareId="postData.shareId"
		:sharedByList="postData.sharedByList"
		:allPostData="postData"
	class="post-comments"/>

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
	name: 'PostViewer',
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
			loadedPostData: {},
			loadedSharedPostData: {}
		}
	},
	methods:{
		toProfile(id_){
			const profileUrl = window.location.href.split("#")[0];
			return profileUrl + "#/profile~" + id_ ;
		},

		toPost(id_){
			const profileUrl = window.location.href.split("#")[0];
			return profileUrl + "#/post~" + id_ ;
		},

		getSharedPostInfo(){
			const postId = parseInt(this.loadedPostData.shareId);
			const token = JSON.parse(localStorage.getItem("yipUserData")).token;
			fetch(this.$ENDPOINT+"/single_post/" + postId, {
					method: 'GET',
					headers: {
						'Authorization': `Bearer ${token}`
					},
				})
				.then(response => response.json())
				.then(data => {
					this.loadedSharedPostData = data.message;
					console.log("data:", this.postData);
				})
				.catch(error => {
					console.error("Error: ", error);
				});
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
			"sharedByList": data.sharedByList,
			"shareId": data.shareId,
			"media": data.media,
			"apiOrigin": data.apiOrigin,
			"nsfwPost": data.nsfwPost,
			"privatePost": data.privatePost,
			"commentCount": data.commentCount,
			"voteHeart": data.voteHeart,
			"voteUp": data.voteUp,
			"voteDown": data.voteDown,
		}

		if(this.loadedPostData.shareId != 0){
			this.getSharedPostInfo();
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
  margin: 2ch 0;
  width: 100%;
  max-width: calc(100vw - 4ch);
  min-width: 512px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 2ch;
  box-shadow: 0px 0px 10px rgba(14, 14, 14, 0.5);
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

.shared{
	width: calc(100% - 4ch);
	margin: 1ch 0;
	background-color: #2A2A2D;
	box-shadow: inset -6px -6px 10px rgba(50, 50, 50, 0.45), inset 6px 6px 10px rgba(18, 18, 18, 0.3);
	border-radius: 1ch;
	padding-bottom: 1.5ch;
}

.shared > div{
	scale: 0.9;
	height: 100% - 1ch;
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