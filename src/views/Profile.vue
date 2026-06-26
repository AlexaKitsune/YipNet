<template>
    <YipNetLayout :user-data="sessionUserData" :on-session="onSession" class="Profile-MAIN">
        <main class="mx-auto max-w-[1080px]">
            <div v-if="loading" class="p-6 opacity-70">
                Loading profile...
            </div>

            <div v-else-if="userData.id">
                <!-- cover -->
                <section class="relative aspect-[3/1] w-full overflow-hidden rounded-b-lg bg-black/30">
                    <img
                        v-if="coverUrl"
                        :src="coverUrl"
                        class="h-full w-full object-cover"
                    >

                    <div v-else class="flex h-full w-full items-center justify-center opacity-50">
                        [ {{ $t('profile.noCover') }} ]
                    </div>

                    <UButton
                        v-if="isOwner"
                        icon="i-lucide-square-pen"
                        color="neutral"
                        variant="soft"
                        class="absolute bottom-3 right-3 z-30"
                        @click="$refs.coverInput.click()"
                    />
					<input
						ref="coverInput"
						type="file"
						accept="image/*"
						class="hidden"
						@change="uploadProfileImage($event, 'cover')"
					/>
                </section>

                <!-- avatar -->
                <section class="relative px-4">
                    <div class="-mt-16 flex items-end gap-4">
                        <div class="relative">
                            <UAvatar
                                :src="avatarUrl"
                                :alt="authorName"
                                class="size-32 ring-4 ring-[var(--alexicon-bg)]"
                            />

                            <UButton
								v-if="isOwner"
								icon="i-lucide-square-pen"
								color="neutral"
								variant="soft"
								size="xs"
								class="absolute bottom-1 right-1"
								@click="$refs.avatarInput.click()"
							/>
							<input
								ref="avatarInput"
								type="file"
								accept="image/*"
								class="hidden"
								@change="uploadProfileImage($event, 'avatar')"
							/>
                        </div>

                        <div class="pb-2">
                            <h1 class="text-2xl font-bold profile-username">
                                {{ authorName }}
                            </h1>

                            <p class="text-sm text-gray-400">
                                @{{ userData.at_sign || userData.nickname }}
                            </p>
                        </div>
                    </div>
                </section>

                <!-- info -->
                <section class="mt-4 flex flex-col gap-4 px-4 md:flex-row md:items-start md:justify-between">
                    <div class="flex-1">
                        <div v-if="!editingDescription" class="flex items-start gap-2">
                            <p v-if="userData.description" class="whitespace-pre-wrap">
                                {{ userData.description }}
                            </p>

                            <p v-else class="italic opacity-50">
                                {{ isOwner ? $t('profile.addDescription') : 'No description' }}
                            </p>

                            <UButton
                                v-if="isOwner"
                                icon="i-lucide-square-pen"
                                variant="ghost"
                                color="neutral"
                                size="xs"
                                @click="startEditDescription"
                            />
                        </div>

                        <div v-else class="max-w-md space-y-2">
							<UTextarea
								v-model="descriptionInput"
								maxlength="255"
								autoresize
								:rows="3"
								class="w-full"
								:ui="{ base: 'w-full bg-black text-white placeholder:text-gray-500' }"
							/>
							<div class="flex justify-end gap-2">
								<UButton color="neutral" variant="ghost" @click="cancelEditDescription">
									Cancel
								</UButton>
								<UButton color="primary" :loading="savingDescription" @click="saveDescription">
									Save
								</UButton>
							</div>
						</div>
                    </div>

                    <div class="flex flex-wrap items-center gap-3">
                        <UButton
                            v-if="!isOwner"
                            icon="i-lucide-message-circle-more"
                            color="neutral"
                            variant="soft"
                            @click="openDirectChat"
                        />

                        <template v-if="!isOwner">
                            <UButton
                                v-if="!userData.viewer?.following"
                                icon="i-lucide-user-plus"
                                color="primary"
                                @click="follow"
                            >
                                {{ $t('profile.btnToFollow') }}
                            </UButton>

                            <UButton
                                v-else
                                icon="i-lucide-user-minus"
                                color="neutral"
                                variant="soft"
                                @click="unfollow"
                            >
                                {{ $t('profile.btnFollowing') }}
                            </UButton>

                            <UButton
                                v-if="!userData.viewer?.blocked"
                                icon="i-lucide-ban"
                                color="error"
                                variant="soft"
                                @click="block"
                            >
                                {{ $t('profile.btnBlock') }}
                            </UButton>

                            <UButton
                                v-else
                                color="error"
                                variant="soft"
                                @click="unblock"
                            >
                                Unblock
                            </UButton>
                        </template>

                        <div class="flex gap-4 text-sm">
                            <p>
                                <b>{{ userData.followers_count || 0 }}</b> {{ $t('profile.followers') }}
                            </p>

                            <p>
                                <b>{{ userData.following_count || 0 }}</b> {{ $t('profile.following') }}
                            </p>
                        </div>
                    </div>
                </section>

                <!-- badges -->
                <section v-if="badges.length" class="mt-6 px-4">
                    <div class="mb-3 flex items-center gap-2">
                        <UIcon name="i-lucide-award" class="size-5 opacity-70" />
                        <h2 class="font-semibold">{{ $t('profile.badges') }}</h2>
                    </div>

                    <div class="badges-grid">
                        <UPopover
                            v-for="badge in badges"
                            :key="badge.id"
                            v-model:open="badge.open"
                            mode="click"
                            :content="{
                                side: 'top',
                                align: 'center',
                                sideOffset: 8,
                                collisionPadding: 16,
                                avoidCollisions: true
                            }"
                            :ui="{
                                content: 'z-[9999] max-w-[calc(100vw-2rem)] bg-[var(--alexicon-surface)] text-[var(--alexicon-text)] border border-white/10 shadow-xl rounded-xl p-0'
                            }"
                        >
                            <div
                                class="badge-card"
                                :class="`badge-rarity-${badge.rarity}`"
                            >
                                <img
                                    :src="badgeImageUrl(badge.image)"
                                    :alt="badge.name"
                                    class="badge-image"
                                >
                            </div>

                            <template #content>
                                <div class="badge-popover">
                                    <UButton
                                        icon="i-lucide-x"
                                        size="xs"
                                        color="neutral"
                                        variant="ghost"
                                        class="badge-popover-close"
                                        @click="badge.open = false"
                                    />

                                    <img
                                        :src="badgeImageUrl(badge.image)"
                                        :alt="badge.name"
                                        class="badge-popover-image"
                                    >

                                    <p class="badge-popover-name">
                                        {{ badge.name }}
                                    </p>

                                    <p class="badge-popover-description">
                                        {{ badge.description || 'No description.' }}
                                    </p>

                                    <p class="badge-popover-meta">
                                        {{ badge.rarity }} · {{ badge.service }}
                                    </p>
                                </div>
                            </template>
                        </UPopover>
                    </div>
                </section>

                <!-- activity + search -->
                <USeparator class="my-6"/>

                <div class="grid grid-cols-2 gap-2 rounded-md bg-transparent">
                    <button class="profile-tab" :class="{ 'profile-tab-active': profileTab === 'activity' }" @click="profileTab = 'activity'">
                        <UIcon name="i-lucide-chart-no-axes-column" /> {{ $t('profile.activity') }}
                    </button>
                    <button class="profile-tab" :class="{ 'profile-tab-active': profileTab === 'search' }" @click="profileTab = 'search'">
                        <UIcon name="i-lucide-search" /> {{ $t('profile.searchPosts') }}
                    </button>
                </div>
                <div class="mt-4">
                    <ContributionGraph v-if="profileTab === 'activity'" :contributions="contributions"/>
                    <YipNetSearch v-else mode="profile" :profile-id="userData.id"/>
                </div>

                <USeparator class="my-6" :label="profileTab == 'search' ? $t('profile.endOfSearch') : ''"/>

                <!-- posts -->
                <section class="space-y-6 px-2" v-if="profileTab != 'search'">
                    <PostRenderer
                        v-for="post in posts"
                        :key="post.id"
                        :post-data="post"
                        @deleted="removePost"
                    />

                    <p v-if="!posts.length" class="text-center opacity-60">
                        No posts yet.
                    </p>
                </section>
            </div>

            <div v-else class="p-6 text-center opacity-70">
                Profile not found.
            </div>
        </main>

        <div class="YipNet-toggle-post-creator" v-if="isOwner && !postCreatorActive" @click="postCreatorActive = true"><UIcon name="i-lucide-square-pen" class="size-6 text-white" /></div>
        <PostCreator v-else-if="isOwner" @close="postCreatorActive = false" @update-post="handlePostCreated"/>

        <ConfirmDialog
            v-model:open="blockConfirmOpen"
            title="Block this user?"
            description="They will no longer be able to interact with you."
            confirm-label="Block"
            confirm-color="error"
            :loading="blockingUser"
            @confirm="confirmBlock"
        />
    </YipNetLayout>
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL

import YipNetLayout from '@/layouts/YipNetLayout.vue'
import PostRenderer from '@/components/PostRenderer.vue'
import ContributionGraph from '@/components/ContributionGraph.vue'
import YipNetSearch from '@/components/YipNetSearch.vue'
import PostCreator from '@/components/PostCreator.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { getOrCreateDirectConversation } from '@/services/yipnet/messages'
import { getProfileContributions } from '@/services/yipnet/stats'
import { getUserPosts } from '@/services/yipnet/posts'
import { followUser, unfollowUser, blockUser, unblockUser } from '@/services/alexicon/social'
import { getUser, updateProfile, uploadAvatar, uploadCover } from '@/services/alexicon/users'
import { uploadFile } from '@/services/alexicon/media'
import { getUserBadges } from '@/services/alexicon/badges'

export default {
    name: 'Profile',
    components: {
        YipNetLayout,
        PostRenderer,
        ContributionGraph,
        YipNetSearch,
        PostCreator,
        ConfirmDialog,
    },
    props: {
        sessionUserData: {
            type: Object,
            default: () => ({})
        },
        onSession: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            userData: {},
            posts: [],
            loading: false,
            savingDescription: false,
            editingDescription: false,
            descriptionInput: '',
            currentUserId: localStorage.getItem('alexicon_user_id'),
            contributions: [],
            profileTab: 'activity',
            postCreatorActive: false,
            badges: [],
            blockConfirmOpen: false,
            blockingUser: false,
        }
    },
    computed: {
        username() {
            return this.$route.params.username
        },

        profileId() {
            return this.$route.params.id
        },

        isOwner() {
            return Number(this.userData.id) === Number(this.currentUserId)
        },

        authorName() {
            return `${this.userData.name || ''} ${this.userData.surname || ''}`.trim()
        },

        avatarUrl() {
			if (!this.userData.profile_pic) return '';
			if (String(this.userData.profile_pic).startsWith('/'))
				return `${API_URL}${this.userData.profile_pic}`;
			return `${API_URL}/alexicon/media/${this.userData.profile_pic}`;
		},

		coverUrl() {
			if (!this.userData.cover_pic) return '';
			if (String(this.userData.cover_pic).startsWith('/'))
				return `${API_URL}${this.userData.cover_pic}`;
			return `${API_URL}/alexicon/media/${this.userData.cover_pic}`;
		},
    },

    methods: {
        async loadProfile() {
            this.loading = true

            try {
                const userResult = await getUser(this.profileId)
                this.userData = userResult.data || userResult

                const postResult = await getUserPosts(this.userData.id)
                this.posts = postResult.data?.posts || []

                const contributionsResult = await getProfileContributions(this.userData.id)
                this.contributions = contributionsResult.data?.contributions || []

                const badgesResult = await getUserBadges(this.userData.id)

                this.badges = (badgesResult.data?.badges || []).map(badge => ({
                    ...badge,
                    open: false
                }))
            } finally {
                this.loading = false
            }
        },

        startEditDescription() {
            this.descriptionInput = this.userData.description || ''
            this.editingDescription = true
        },

        cancelEditDescription() {
            this.descriptionInput = ''
            this.editingDescription = false
        },

        async saveDescription() {
            this.savingDescription = true

            try {
                await updateProfile({
                    description: this.descriptionInput
                })

                this.userData.description = this.descriptionInput
                this.editingDescription = false
            } finally {
                this.savingDescription = false
            }
        },

        async follow() {
            await followUser(this.userData.id)
            this.userData.viewer = {
                ...(this.userData.viewer || {}),
                following: true
            }
            this.userData.followers_count = Number(this.userData.followers_count || 0) + 1
        },

        async unfollow() {
            await unfollowUser(this.userData.id)
            this.userData.viewer = {
                ...(this.userData.viewer || {}),
                following: false
            }
            this.userData.followers_count = Math.max(Number(this.userData.followers_count || 0) - 1, 0)
        },

        block() {
            this.blockConfirmOpen = true
        },

        async confirmBlock() {
            this.blockingUser = true

            try {
                await blockUser(this.userData.id)
                this.blockConfirmOpen = false
                this.$router.push('/')
            } finally {
                this.blockingUser = false
            }
        },

        async unblock() {
            await unblockUser(this.userData.id)
            this.userData.viewer = {
                ...(this.userData.viewer || {}),
                blocked: false
            }
        },

        removePost(postId) {
            this.posts = this.posts.filter(post => Number(post.id) !== Number(postId))
        },

		async uploadProfileImage(event, type) {
			const file = event.target.files?.[0]
			if (!file) return

			try {
				const userId = localStorage.getItem('alexicon_user_id')
				const targetPath = `yipnet/${userId}/profile/`

				const uploadResult = await uploadFile(file, {
					targetPath,
					visibility: 'public'
				})

				const fileId =
					uploadResult.data?.fileId ||
					uploadResult.fileId ||
					uploadResult.data?.id ||
					uploadResult.id

				if (!fileId) {
					throw new Error('No se recibió el ID del archivo.')
				}

				const result = type === 'avatar'
					? await uploadAvatar(fileId)
					: await uploadCover(fileId)

				if (type === 'avatar') {
					this.userData.profile_pic = result.data?.profile_pic
				} else {
					this.userData.cover_pic = result.data?.cover_pic
				}

				await this.loadProfile()
			} finally {
				event.target.value = ''
			}
		},

        async openDirectChat() {
            const result = await getOrCreateDirectConversation(this.userData.id)
            const conversationId = result.data?.conversation_id
            if (conversationId) {
                this.$router.push(`/chat/${conversationId}`)
            }
        },

        async handlePostCreated() {
            this.postCreatorActive = false
            await this.loadProfile()
        },

        badgeImageUrl(value) {
            if (!value) return ''
            if (String(value).startsWith('http')) {
                return value
            }
            if (String(value).startsWith('/')) {
                return `${API_URL}${value}`
            }
            return `${API_URL}/alexicon/media/${value}`
        },
    },

    mounted() {
        this.loadProfile()
    },

    watch: {
        '$route.params.id'() {
            this.loadProfile()
        }
    },
}
</script>

<style scoped lang="stylus">
.profile-username
    text-shadow: 0 0 6px black

.profile-tab
    display flex
    align-items center
    justify-content center
    gap 0.5ch
    padding 0.75ch 1ch
    border-radius 6px
    color #9ca3af
    background transparent
    transition all 0.15s

    &:hover
        background #3a3a3a
        color white

.profile-tab-active
    background #3a3a3a
    color white

.YipNet-toggle-post-creator
    background-color: #7701ff
    position: fixed
    width: 50px
    aspect-ratio: 1/1
    right: 15px
    bottom: 15px
    border-radius: 100vw
    display: flex
    flex-direction: column
    align-items: center
    justify-content: center
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.25)
    z-index: 1

    &:hover
        cursor: pointer
        scale: 1.1
        transition: all 0.1s

/* badges */
.badges-grid
    display grid
    grid-template-columns repeat(auto-fill, minmax(64px, 64px))
    gap 0.75rem

.badge-card
    width 64px
    aspect-ratio 1 / 1
    display flex
    align-items center
    justify-content center
    border-radius 12px
    //background rgba(0, 0, 0, 0.25)
    //border 1px solid rgba(255, 255, 255, 0.08)
    //box-shadow 0 0 1ch rgba(0, 0, 0, 0.25)
    transition all 0.15s

    &:hover
        transform translateY(-2px) scale(1.04)
        background rgba(255, 255, 255, 0.08)

.badge-image
    width 100%
    height 100%
    object-fit contain

/*
.badge-rarity-common
    border-color rgba(156, 163, 175, 0.35)

.badge-rarity-rare
    border-color rgba(59, 130, 246, 0.55)

.badge-rarity-epic
    border-color rgba(168, 85, 247, 0.65)

.badge-rarity-legendary
    border-color rgba(250, 204, 21, 0.75)
    box-shadow 0 0 1.2ch rgba(250, 204, 21, 0.18)
*/
.badge-popover
    position relative
    width 280px
    max-width calc(100vw - 2rem)
    padding 1rem
    display flex
    flex-direction column
    align-items center
    gap 0.75rem

.badge-popover-image
    width 256px
    height 256px
    max-width calc(100vw - 4rem)
    max-height calc(100vw - 4rem)
    object-fit contain

.badge-popover-close
    position absolute
    top 0.5rem
    right 0.5rem
    z-index 2

.badge-popover-name
    font-size 1.1rem
    font-weight 700
    margin 0
    text-align center

.badge-popover-description
    margin 0
    font-size 0.85rem
    opacity 0.75
    line-height 1.35
    text-align center

.badge-popover-meta
    margin 0
    font-size 0.7rem
    opacity 0.45
    text-transform uppercase
    letter-spacing 0.08em
</style>