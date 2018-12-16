<template>
  <div id="app">
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0">
    <vue-snotify/>
    <b-container
      class="container-fluid"
      fluid
    >
      <b-row>
        <b-col :cols="12">
          <router-view id="routerview-main"/>
        </b-col>
      </b-row>
    </b-container>


    <br>
    <hr>
    <scroll-to-top/>
  </div>
</template>

<script>
import ScrollToTop from '@/components/Snippets/ScrollToTop';

export default {
  components: { ScrollToTop },
  created() {
  },
  metaInfo: {
    title: 'Atlantis',
    titleTemplate: (titleChunk) => {
      const suffix = '';
      return titleChunk ? `${titleChunk} ${suffix}` : suffix;
    },
  },
};
</script>

<style>
.container-first {
  padding-top: 2rem;
}

.cursor-pointer {
  cursor: pointer;
}

.link-as-text {
  color: #212529;
}

.link-as-text:hover,
.link-as-text:focus {
  text-decoration: none;
}

.overflow-x {
  overflow-x: scroll;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.td-no-border td {
  border: none;
}

.td-no-wrap td {
  white-space: nowrap;
}

.table-hidden {
  display: none;
}
</style>

<style lang="scss">
@import "node_modules/bootstrap/scss/functions";
@import "node_modules/bootstrap/scss/variables";
@import "node_modules/bootstrap/scss/mixins";
</style>
