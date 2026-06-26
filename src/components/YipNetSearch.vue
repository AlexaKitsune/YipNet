<template>
    <UCard
        class="YipNetSearch-MAIN bg-black/20 border-0"
        :ui="{ root: 'border-0', body: 'space-y-4' }"
        variant="ghost"
    >
        <div class="grid gap-3 md:grid-cols-[1fr_auto_auto]">
            <UInput
                v-model="search.q"
                icon="i-lucide-search"
                :placeholder="$t('search.placeholder')"
                variant="none"
                class="w-full"
                :ui="{ base: 'bg-black text-white placeholder:text-gray-500 rounded-md' }"
                @keyup.enter="doSearch"
            />

            <UInput
                v-model="search.from"
                type="date"
                variant="none"
                :ui="{ base: 'bg-black text-white rounded-md' }"
            />

            <UInput
                v-model="search.to"
                type="date"
                variant="none"
                :ui="{ base: 'bg-black text-white rounded-md' }"
            />
        </div>

        <!-- switches -->
        <UCard class="bg-black/20 border-0" :ui="{ body: 'space-y-4' }" variant="ghost">

            <div class="grid gap-3 md:grid-cols-3">
                <section class="search-filter-group">
                    <p class="search-filter-title">{{ $t('search.content') }}</p>

                    <label class="search-switch">
                        <USwitch v-model="search.include_files" />
                        <span>{{ $t('search.includesFiles') }}</span>
                    </label>

                    <label class="search-switch">
                        <USwitch v-model="search.include_urls" />
                        <span>{{ $t('search.includesURLs') }}</span>
                    </label>
                </section>

                <section class="search-filter-group">
                    <p class="search-filter-title">{{ $t('search.filters') }}</p>

                    <label class="search-switch">
                        <USwitch v-model="search.ai_generated" />
                        <span>{{ $t('search.AIGenerated') }}</span>
                    </label>

                    <label class="search-switch">
                        <USwitch v-model="search.nsfw" />
                        <span>NSFW</span>
                    </label>
                </section>

                <section class="search-filter-group">
                    <p class="search-filter-title">Search</p>

                    <label class="search-switch">
                        <USwitch v-model="search.case_sensitive" />
                        <span>{{ $t('search.caseSensitive') }}</span>
                    </label>
                </section>
            </div>

            <div class="flex items-center gap-2">
                <UButton icon="i-lucide-search" color="neutral" :loading="loading" @click="doSearch">
                    {{ $t('search.searchButton') }}
                </UButton>

                <UButton variant="ghost" color="neutral" @click="resetSearch">
                    {{ $t('search.reset') }}
                </UButton>
            </div>
        </UCard>

        <!-- users -->
        <div v-if="results.users.length" class="space-y-3">
            <h2 class="font-semibold">{{ $t('search.users') }}</h2>
            <RouterLink
                v-for="user in results.users"
                :key="user.id"
                :to="`/user/${user.id}`"
                class="flex items-center gap-3 rounded-lg bg-black/20 p-3 hover:bg-[#3a3a3a]"
            >
                <UAvatar :src="userAvatar(user)" />

                <div class="min-w-0">
                    <p class="font-semibold">
                        {{ user.name }} {{ user.surname }}
                    </p>
                    <p class="text-sm opacity-60">
                        @{{ user.at_sign || user.nickname }}
                    </p>
                    <p v-if="user.description" class="truncate text-sm opacity-70">
                        {{ user.description }}
                    </p>
                </div>
            </RouterLink>
        </div>

        <h2 class="font-semibold" v-if="results.posts.length && mode == 'global'">{{ $t('search.posts') }}</h2>
        <PostRenderer v-for="post in results.posts" :key="post.id" :post-data="post"/>
    </UCard>
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL
import PostRenderer from '@/components/PostRenderer.vue'

import {
    searchGlobal,
    searchProfile
} from '@/services/yipnet/search'

export default {
    name: 'YipNetSearch',
    components: {
        PostRenderer,
    },
    props: {
        initialQ: {
            type: String,
            default: ''
        },
        mode: {
            type: String,
            default: 'global'
        },
        profileId: {
            type: Number,
            default: null
        },
    },
    data() {
        return {
            loading: false,
            searched: false,
            search: {
                q: '',
                type: 'all',
                from: '',
                to: '',
                include_files: false,
                include_urls: false,
                case_sensitive: false,
                ai_generated: false,
                nsfw: false
            },
            results: {
                users: [],
                posts: []
            }
        }
    },
    computed: {
        hasResults() {
            return (
                this.results.users.length ||
                this.results.posts.length
            )
        }
    },
    methods: {
        resetSearch() {
            this.search = {
                q: '',
                type: 'all',
                from: '',
                to: '',
                include_files: false,
                include_urls: false,
                case_sensitive: false,
                ai_generated: false,
                nsfw: false
            };
            this.results = {
                users: [],
                posts: []
            };
            this.searched = false;
        },

        buildParams() {
            return {
                ...this.search,
                include_files: this.search.include_files ? '1' : '',
                include_urls: this.search.include_urls ? '1' : '',
                case_sensitive: this.search.case_sensitive ? '1' : '',
                ai_generated: this.search.ai_generated ? '1' : '',
                nsfw: this.search.nsfw ? '1' : ''
            }
        },

        async doSearch() {
            this.loading = true

            try {
                let result
                const params = this.buildParams()

                if (this.mode === 'profile') {
                    result = await searchProfile(this.profileId, params)

                    this.results = {
                        users: [],
                        posts: result.data?.posts || []
                    }
                } else {
                    result = await searchGlobal(params)

                    this.results = {
                        users: result.data?.users || [],
                        posts: result.data?.posts || []
                    }
                }

                this.searched = true
            } finally {
                this.loading = false
            }
        },

        userAvatar(user) {
            if (!user.profile_pic) return ''
            if (String(user.profile_pic).startsWith('/'))
                return `${API_URL}${user.profile_pic}`
            return `${API_URL}/alexicon/media/${user.profile_pic}`
        },
    },
    mounted() {
        if (this.initialQ) {
            this.search.q = this.initialQ
            this.doSearch()
        }
    },
    watch: {
        initialQ(newValue) {
            this.search.q = newValue || ''

            if (this.search.q.trim()) {
                this.doSearch()
            }
        }
    },
}
</script>

<style scoped lang="stylus">
.search-filter-group
    background rgba(0, 0, 0, 0.18)
    //border 1px solid rgba(255, 255, 255, 0.06)
    border-radius 10px
    padding 1rem
    min-height 120px

.search-filter-title
    font-size 0.72rem
    text-transform uppercase
    letter-spacing 0.12em
    opacity 0.45
    margin-bottom 0.85rem

.search-switch
    display flex
    align-items center
    gap 0.65rem
    font-size 0.9rem
    white-space nowrap
    margin-bottom 0.7rem
</style>