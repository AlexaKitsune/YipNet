<template>
	<main class="YipNet-MAIN">

	<AlexiconComponent :type="'universalloginregister'" :serviceName="'YipNet'" v-if="!sessionActive" @get-val="() => { sessionActive = true }" @login-register-err="(val) => launchEmergent(val, 'login-register-err')"/>
	<AlexiconComponent :type="'mainpage'" :highlightBtnColor="'#7701ff'" v-else>
		<AlexiconComponent :type="'searchbar'" :placeholder="'Search'" @get-switch-menu="(val) => menuActive = val">
			<a :href="getFrontURL()" class="YipNet-icon-newsfeed"><Newspaper/></a>
			<a :href="getFrontURL()+'/settings/'" class="YipNet-icon-settings"><Settings/></a>
			<a :href="getFrontURL()+'/notifications/'" class="YipNet-icon-notif">
				<Bell/>
				<div v-if="notifications-1 > 0">{{ notifications >= 100 ? '99+' : notifications-1 }}</div>
			</a>
			<a :href="getFrontURL()+'/profile/'+AlexiconUserData.userData.id" class="YipNet-profile-icon">
				<ImageProtected :mediaId="AlexiconUserData.userData.current_profile_pic"/>
			</a>
		</AlexiconComponent>
		<div class="Alexicon-container">
			<AlexiconComponent :type="'asidemenu'" :active="menuActive" :size="200"></AlexiconComponent>
			<main class="Alexicon-main">

				<div class="YipNet-toggle-post-creator" v-if="!postCreatorActive" @click="postCreatorActive = true" v-show="route != 'chat'"><SquarePen color="#ffffff"/></div>
				<PostCreator v-else @close="closePostCreator" @update-post="() => profileRefreshTick++"/>
				<NewsFeed v-if="route == ''"/>
				<SinglePost v-if="route == 'post'"/>
				<ProfileUser v-if="route  == 'profile'" :get-image-url="getImageURL" :refreshTick="profileRefreshTick" />
				<SettingsConfig v-if="route == 'settings'"/>
				<NotificationsWindow v-show="route == 'notifications'" @update-notifications="(val) => notifications = val"/>
				<ChatWindow v-if="route == 'chat'"/>
				
			</main>
		</div>
	</AlexiconComponent>

	<AlexiconComponent v-if="emergent.active" :type="'emergent'" @close="emergent.active = false">
		<div class="YipNet-emergent">
			<TriangleAlert v-if="emergent.origin == 'login-register-err'" color="red"/>
			<p v-if="emergent.origin == 'login-register-err'">{{ emergent?.message?.response }}</p>
			<button class="highlighted-btn" @click="emergent.active = false">Ok</button>
			<br>
		</div>
	</AlexiconComponent>

	</main>
</template>

<script>
import AlexiconComponent from './AlexiconComponents/AlexiconComponent.vue';
import PostCreator from './comp/PostCreator.vue';
import NewsFeed from './views/NewsFeed.vue';
import SinglePost from './views/SinglePost.vue';
import ProfileUser from './views/ProfileUser.vue';
import SettingsConfig from './views/SettingsConfig.vue';
import { SquarePen, Newspaper, Settings, Bell, TriangleAlert } from 'lucide-vue-next';
import NotificationsWindow from './views/NotificationsWindow.vue';
import ChatWindow from './views/ChatWindow.vue';
import ImageProtected from './comp/ImageProtected.vue';

export default {
	name: 'YipNet',
	components: {
		AlexiconComponent,
		PostCreator,
		NewsFeed,
		SinglePost,
		ProfileUser,
		SettingsConfig,
		NotificationsWindow,
		ChatWindow,
		SquarePen,
		Newspaper,
		Settings,
		Bell,
		TriangleAlert,
		ImageProtected,
	},
	data(){
		return{
			AlexiconUserData: {},
			sessionActive: false,
			menuActive: false,
			route: "",
			postCreatorActive: false,
			notifications: 0,
			activeEmergent: false,
			emergent: {
				active: false,
				origin: '',
				message: '',
			},
			profileRefreshTick: 0,
		}
	},
	methods: {
		autoRoutes(){
			const path = new URL(window.location.href).pathname;
			let pathArray = path.split("/");
			// eslint-disable-next-line
			let x = pathArray.shift();
			this.route = pathArray[0];
		},

		getFrontURL(){
			return window.location.origin;
		},

		closePostCreator(){
			this.postCreatorActive = false;
		},

		launchEmergent(val_, origin_){
			this.emergent.active = true;
			this.emergent.origin = origin_;
			this.emergent.message = val_;
		},
	},

	watch: {
		sessionActive(newValue) {
			if (newValue) {
				this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
			}
		}
	},

	mounted(){
		this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
		this.autoRoutes();
		window.addEventListener("popstate", this.autoRoutes);
	},

	created() {
		const originalPushState = history.pushState;
		const originalReplaceState = history.replaceState;
		const triggerAutoRoutes = () => this.autoRoutes();
		history.pushState = function(...args) {
			originalPushState.apply(this, args);
			triggerAutoRoutes();
		};
		history.replaceState = function(...args) {
			originalReplaceState.apply(this, args);
			triggerAutoRoutes();
		};
	},

	beforeUnmount() {
		window.removeEventListener("popstate", this.autoRoutes);
	}
}
</script>

<style>
button{
	color: light-dark(black, white);
	background-color: light-dark(#efedea, #6b6b6b);
	border: none;
	border-radius: 5px;
	padding: 0.5ch 1ch;
	min-width: 10ch;
	cursor: pointer;
}

*{	
	scroll-behavior: smooth;
}
</style>

<style scoped>
.YipNet-icon-newsfeed{
	margin-left: -40px;
}

.YipNet-icon-newsfeed, .YipNet-icon-settings, .YipNet-icon-notif{
	margin-right: 10px;
	transition: all 0.1s;
	margin-bottom: -4px;
}

.YipNet-icon-newsfeed:hover, .YipNet-icon-settings:hover, .YipNet-icon-notif:hover{
	cursor: pointer;
	scale: 1.1;
}

.YipNet-icon-newsfeed > *, .YipNet-icon-settings > *, .YipNet-icon-notif > *{
	color: light-dark(black, white);
}

.YipNet-icon-notif{
	position: relative;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-bottom: -1px;
}

.YipNet-icon-notif > div{
	position: absolute;
	background-color: red;
	color: white;
	border-radius: 100vw;
	padding: 0 2px;
	font-size: 10px;
	top: 0;
	left: 0;
}

.YipNet-profile-icon{
	height: 40px;
	display: flex;
	align-items: center;
	margin-right: 12px;
	margin-right: 40px;
}

.YipNet-profile-icon > img{
	height: 65%;
	aspect-ratio: 1/1;
	object-fit: cover;
	object-position: center;
	border-radius: 100vw;
}

.YipNet-toggle-post-creator{
	background-color: #7701ff;
	position: fixed;
	width: 50px;
	aspect-ratio: 1/1;
	right: 15px;
	bottom: 15px;
	border-radius: 100vw;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	box-shadow: 0 0 15px rgba(0, 0, 0, 0.25);
	z-index: 1;
}

.YipNet-toggle-post-creator:hover{
	cursor: pointer;
	scale: 1.1;
	transition: all 0.1s;
}

/* emergent */
.YipNet-emergent{
	display: flex;
	flex-direction: column;
	align-items: center;
}
</style>