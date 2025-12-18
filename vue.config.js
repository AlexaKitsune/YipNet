const path = require("path");
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: "/yipnet/",
  outputDir: path.resolve(__dirname, "../Alexicon/public/yipnet"),
})
