<template>
    <!--Basic components-->
    <AlexiconText v-if="type == 'text'" :styles="styles" :val="val" :placeholder="placeholder" :disabled="disabled" @get-val="updateValue"/>
    <AlexiconButton v-if="type == 'button'" :styles="styles" :disabled="disabled"><slot></slot></AlexiconButton>
    <AlexiconRange v-if="type == 'range'" :styles="styles" :disabled="disabled" :step="step" :min="min" :max="max" :val="val" @get-val="updateValue"/>
    <AlexiconCheckbox v-if="type == 'checkbox'" :styles="styles" :disabled="disabled" :checked="checked" @get-val="updateValue"/>
    <AlexiconRadio v-if="type == 'radio'" :styles="styles" :disabled="disabled" :checked="checked" @get-val="updateValue"/>
    <AlexiconSwitch v-if="type == 'switch'" :styles="styles" :disabled="disabled" :checked="checked" @get-val="updateValue"/>
    <AlexiconColor v-if="type == 'color'" :styles="styles" :val="val" :standalone="standalone" @get-val="updateValue"/>
    <AlexiconKnob v-if="type == 'knob'" :styles="styles" :disabled="disabled" :step="step" :min="min" :max="max" :val="val" @get-val="updateValue"/>
    <AlexiconMicroKnob v-if="type == 'microknob'" :styles="styles" :disabled="disabled" :step="step" :min="min" :max="max" :val="val" @get-val="updateValue"/>
    <AlexiconMedia v-if="type=='video'" :styles="styles" :type="type" :src="src" :autoplay="autoplay" :loop="loop" :framerate="framerate" :subtitles="subtitles" @get-play-pause="(val) => updateSpecificValue(val, 'get-play-pause')" @get-current-time="(val) => updateSpecificValue(val, 'get-current-time')" @get-seek="(val) => updateSpecificValue(val, 'get-seek')" @get-cc="(val) => updateSpecificValue(val, 'get-cc')" @get-loop="(val) => updateSpecificValue(val, 'get-loop')"/>
    <AlexiconMedia v-if="type=='audio'" :styles="styles" :type="type" :src="src" :autoplay="autoplay" :loop="loop" @get-play-pause="(val) => updateSpecificValue(val, 'get-play-pause')" @get-current-time="(val) => updateSpecificValue(val, 'get-current-time')" @get-seek="(val) => updateSpecificValue(val, 'get-seek')" @get-loop="(val) => updateSpecificValue(val, 'get-loop')"/>
    <AlexiconCode v-if="type=='code'" :styles="styles" :val="val"/>
    <AlexiconMarkdown v-if="type=='markdown'" :val="val"/>
    <AlexiconWindow v-if="type=='window'" :styles="styles" :title="title" :initialPosition="initialPosition"><slot></slot></AlexiconWindow>
    <AlexiconDoc v-if="type=='doc'" :styles="styles" :src="src"/>
    <AlexiconTextarea v-if="type == 'textarea'" :styles="styles" :val="val" :placeholder="placeholder" :disabled="disabled" :standalone="standalone" :resize="resize" :maxlength="maxlength" @get-val="updateValue"/>
    <!--Advanced components-->
    <AlexiconMainpage v-if="type == 'mainpage'" :highlightBtnColor="highlightBtnColor"><slot></slot></AlexiconMainpage>
    <AlexiconSearchbar v-if="type == 'searchbar'" :styles="styles" :val="val" :placeholder="placeholder" :disabled="disabled" :bgcolor="bgcolor" @get-switch-menu="(val) => updateSpecificValue(val, 'get-switch-menu')"><slot></slot></AlexiconSearchbar>
    <AlexiconAsidemenu v-if="type == 'asidemenu'" :active="active" :size="size"><slot></slot></AlexiconAsidemenu>
    <AlexiconUniversalLoginRegister v-if="type == 'universalloginregister'" :styles="styles" :serviceName="serviceName" :txtColor="txtColor" :bgImg="bgImg" @activate-session="updateValue"/>
</template>

<script>
//Basic components:
import AlexiconText from './BasicComponents/AlexiconText.vue';
import AlexiconButton from './BasicComponents/AlexiconButton.vue';
import AlexiconRange from './BasicComponents/AlexiconRange.vue';
import AlexiconCheckbox from './BasicComponents/AlexiconCheckbox.vue';
import AlexiconRadio from './BasicComponents/AlexiconRadio.vue';
import AlexiconSwitch from './BasicComponents/AlexiconSwitch.vue';
import AlexiconColor from './BasicComponents/AlexiconColor.vue';
import AlexiconKnob from './BasicComponents/AlexiconKnob.vue';
import AlexiconMicroKnob from './BasicComponents/AlexiconMicroKnob.vue';
import AlexiconMedia from './BasicComponents/AlexiconMedia.vue';
import AlexiconCode from './BasicComponents/AlexiconCode.vue';
import AlexiconMarkdown from './BasicComponents/AlexiconMarkdown.vue';
import AlexiconWindow from './BasicComponents/AlexiconWindow.vue';
import AlexiconDoc from './BasicComponents/AlexiconDoc.vue';
import AlexiconTextarea from './BasicComponents/AlexiconTextarea.vue';
//Advanced components:
import AlexiconMainpage from './AdvancedComponents/AlexiconMainpage.vue';
import AlexiconSearchbar from './AdvancedComponents/AlexiconSearchbar.vue';
import AlexiconAsidemenu from './AdvancedComponents/AlexiconAsidemenu.vue';
import AlexiconUniversalLoginRegister from './AdvancedComponents/AlexiconUniversalLoginRegister.vue';

export default {
    name: 'AlexiconComponent',
    components: {
        //Basic components:
        AlexiconText,
        AlexiconButton,
        AlexiconRange,
        AlexiconCheckbox,
        AlexiconRadio,
        AlexiconSwitch,
        AlexiconColor,
        AlexiconKnob,
        AlexiconMicroKnob,
        AlexiconMedia,
        AlexiconCode,
        AlexiconMarkdown,
        AlexiconWindow,
        AlexiconDoc,
        AlexiconTextarea,
        //Advanced components:
        AlexiconMainpage,
        AlexiconSearchbar,
        AlexiconAsidemenu,
        AlexiconUniversalLoginRegister,
    },
    props:{
        type: String,
        val: undefined,
        title: undefined,
        placeholder: String,
        disabled: Boolean,
        checked: Boolean,
        step: Number,
        min: Number,
        max: Number,
        src: String,
        subtitles: String,
        autoplay: Boolean,
        loop: Boolean,
        framerate: Number,
        initialPosition: Array,
        doc: String,
        standalone: Boolean,
        maxlength: Number,
        //Advanced props:
        bgcolor: Array,
        active: Boolean,
        size: undefined,
        resize: Boolean,
        serviceName: String,
        txtColor: String,
        bgImg: String,
        highlightBtnColor: String,
    },
    data(){
        const purple = '#7700ff';
        const softlightgray = '#dddddd';
        const hardlightgray = '#aaaaaa';
        const blackbg = "rgb(30, 30, 30)";
        const softdarkgray = "#7b7d7d";
        const harddarkgray = "#4c4c4c";
        return{
            styles:{
                light:{
                    text:{
                        default:{
                            bg: 'white',
                            txt: 'black',
                            border: softlightgray,
                        },
                        disabled:{
                            bg: 'white',
                            txt: hardlightgray,
                            border: softlightgray,
                        }
                    },
                    button:{
                        default:{
                            bg: purple,
                            txt: 'white',
                        },
                        disabled:{
                            bg: softlightgray,
                            txt: 'white',
                        }
                    },
                    range:{
                        default:{
                            bg: softlightgray,
                            step: softlightgray,
                            thumb: purple,
                        },
                        disabled:{
                            thumb: hardlightgray,
                        }
                    },
                    checkbox:{
                        default:{
                            bg: softlightgray,
                            check: 'transparent',
                        },
                        checked:{
                            bg: softlightgray,
                            check: purple,
                        },
                        disabled:{
                            bg: softlightgray,
                            check: hardlightgray,
                        },
                        checkedDisabled:{
                            bg: softlightgray,
                            check: hardlightgray,
                        }
                    },
                    radio:{
                        default:{
                            bg: softlightgray,
                            check: 'transparent',
                        },
                        checked:{
                            bg: softlightgray,
                            check: purple,
                        },
                        disabled:{
                            bg: softlightgray,
                            check: hardlightgray,
                        },
                        checkedDisabled:{
                            bg: softlightgray,
                            check: hardlightgray,
                        }
                    },
                    switch:{
                        default:{
                            bg: softlightgray,
                            check: hardlightgray,
                        },
                        checked:{
                            bg: softlightgray,
                            check: purple,
                        },
                        disabled:{
                            bg: softlightgray,
                            check: hardlightgray,
                        },
                    },
                    color:{
                        bg: 'white',
                        txt: 'black',
                        border: softlightgray,
                    },
                    knob:{
                        default:{
                            bg: softlightgray,
                            step: softlightgray,
                            thumb: purple,
                        },
                        disabled:{
                            bg: softlightgray,
                            step: softlightgray,
                            thumb: hardlightgray,
                        }
                    },
                    media:{
                        bg: hardlightgray,
                        progress: purple,
                        thumb: 'white',
                    },
                    window:{
                        inactive: {
                            bar: 'white',
                            txt: 'black',
                        },
                        active: {
                            bar: purple,
                            txt: 'white',
                        }
                    },
                    doc:{
                        label: softlightgray,
                        txt: 'black',
                    },
                    LoginRegister:{
                        bg: "rgb(242, 242, 242)"
                    }
                },
                dark:{
                    text:{
                        default:{
                            bg: 'black',
                            txt: 'white',
                            border: 'transparent',
                        },
                        disabled:{
                            bg: 'black',
                            txt: harddarkgray,
                            border: 'transparent',
                        }
                    },
                    button:{
                        default:{
                            bg: purple,
                            txt: 'white',
                        },
                        disabled:{
                            bg: harddarkgray,
                            txt: softdarkgray,
                        }
                    },
                    range:{
                        default:{
                            bg: harddarkgray,
                            step: harddarkgray,
                            thumb: purple,
                        },
                        disabled:{
                            thumb: harddarkgray,
                        }
                    },
                    checkbox:{
                        default:{
                            bg: harddarkgray,
                            check: 'transparent',
                        },
                        checked:{
                            bg: harddarkgray,
                            check: 'white',
                        },
                        disabled:{
                            bg: harddarkgray,
                            check: softdarkgray,
                        },
                        checkedDisabled:{
                            bg: harddarkgray,
                            check: softdarkgray,
                        }
                    },
                    radio:{
                        default:{
                            bg: harddarkgray,
                            check: 'transparent',
                        },
                        checked:{
                            bg: harddarkgray,
                            check: 'white',
                        },
                        disabled:{
                            bg: harddarkgray,
                            check: softdarkgray,
                        },
                        checkedDisabled:{
                            bg: harddarkgray,
                            check: softdarkgray,
                        }
                    },
                    switch:{
                        default:{
                            bg: harddarkgray,
                            check: 'black'
                        },
                        checked:{
                            bg: purple,
                            check: 'white',
                        },
                        disabled:{
                            bg: harddarkgray,
                            check: softdarkgray,
                        },
                    },
                    color:{
                        bg: blackbg,
                        txt: 'white',
                        border: softlightgray,
                    },
                    knob:{
                        default:{
                            bg: harddarkgray,
                            step: harddarkgray,
                            thumb: 'white',
                        },
                        disabled:{
                            bg: harddarkgray,
                            step: harddarkgray,
                            thumb: softdarkgray,
                        }
                    },
                    media:{
                        bg: hardlightgray,
                        progress: purple,
                        thumb: 'white',
                    },
                    window:{
                        inactive: {
                            bar: 'black',
                            txt: 'white',
                        },
                        active: {
                            bar: purple,
                            txt: 'white',
                        }
                    },
                    doc:{
                        label: harddarkgray,
                        txt: 'white',
                    },
                    LoginRegister:{
                        bg: "#2d2d2d",
                    }
                }
            },
            currentValue: undefined,
        }
    },
    methods: {
        updateValue(value) {
            this.currentValue = value;
            this.$emit('get-val', this.currentValue);
        },

        updateSpecificValue(value, customEvent){
            //console.log("actualizando specific value", customEvent, value)
            this.$emit(customEvent, value);
        },

        vibrate(pattern_){
            try {
                navigator.vibrate(pattern_);
            } catch (error) {
                console.warn("Navigator doesn't support vibration (navigator.vibrate())");
            }
        }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap');

:root {
  color-scheme: light dark;
}

input[type=text], input[type=number], input[type=tel], input[type=email], input[type=password], textarea{
    border: 2px solid light-dark(v-bind('styles.light.text.default.border'), v-bind('styles.dark.text.default.border'));
    color: light-dark(v-bind('styles.light.text.default.txt'), v-bind('styles.dark.text.default.txt'));
    background-color: light-dark(v-bind('styles.light.text.default.bg'), v-bind('styles.dark.text.default.bg'));
    border-radius: 5px;
}

input[type=text]:disabled, input[type=number]:disabled, input[type=tel]:disabled, input[type=email]:disabled, input[type=password]:disabled, textarea:disabled{
    border: 2px solid light-dark(v-bind('styles.light.text.disabled.border'), v-bind('styles.dark.text.disabled.border'));
    color: light-dark(v-bind('styles.light.text.disabled.txt'), v-bind('styles.dark.text.disabled.txt'));
    background-color: light-dark(v-bind('styles.light.text.disabled.bg'), v-bind('styles.dark.text.disabled.bg'));
}

*:not(.Alexicon-unfont){
    font-family: "Roboto Mono", serif;
}

.Alexicon-icon-btn{
    border: none;
    margin: none;
    padding: none;
    width: fit-content;
    height: fit-content;
    background-color: transparent;
}
</style>