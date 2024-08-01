import LoginRegister from './views/LoginRegister.vue';
import NewsFeed from './views/NewsFeed.vue';
import SinglePost from './views/SinglePost.vue';
import ProfileUser from './views/ProfileUser.vue';
import ConfigSettings from './views/ConfigSettings.vue';
import VerifyAccount from './views/VerifyAccount.vue';
import NotFound from './views/NotFound.vue';

const router = [
  { path: '/', component: NewsFeed },
  { path: '/access', component: LoginRegister },
  { path: '/newsfeed', component: NewsFeed },
  { path: '/profile', component: ProfileUser },
  { path: '/post', component: SinglePost },
  { path: '/settings', component: ConfigSettings },
  { path: '/verify', component: VerifyAccount },
  { path: '/*', component: NotFound }
];

export default router;
