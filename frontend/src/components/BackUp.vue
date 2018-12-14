
<template>
  <div>
    {{ lyrics }}
    <b-form-select
      v-model="columns"
      :options="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
      class="mb-3" />
    <b-form-input
      v-model="word"
      type="text"/>
    <b-row>
      <b-col
        v-for="(a, c) in slicedLyrics"
        :key="a[0] + c">
        <b-list-group>
          <b-list-group-item
            v-for="(w, i) in a"
            :key="w + i"
            class="text-center px-1 py-1">
            {{ w }}
          </b-list-group-item>
        </b-list-group>
      </b-col>
    </b-row>


  </div>
</template>

<script>

const _ = require('lodash');

export default {
  components: {
  },
  data: () => ({
    lyrics: '',
    lyricsLower: [],
    lyricsText: [],
    foundLyrics: [],
    word: '',
    columns: 5,
  }),
  computed: {
    slicedLyrics() {
      const arrays = [];
      const l = _.map(this.stableCopy, _.clone);
      const size = Math.ceil(l.length / (this.columns * 1.0));
      this.$snotify.error(size, { timeout: 0 });
      while (l.length > 0) { arrays.push(l.splice(0, size)); }
      return arrays;
    },
  },
  watch: {
    word: {
      handler(word) {
        return word;
      },
      deep: true,
    },
  },
  created() {
    this.loadLyrics();
    this.prepLyrics();
  },
  mounted() {
  },
  methods: {
    prepLyrics() {
      let lyrics = this.lyrics.replace(/[\n\s]/g, ' ');
      while (lyrics.includes('  ')) {
        lyrics = lyrics.replace('  ', ' ');
      }
      lyrics = lyrics.replace(/[^a-zA-Z0-9' ]/g, '');
      this.lyricsLower = lyrics.toLowerCase();
      this.lyricsText = this.lyricsLower.toLowerCase().replace("'", '');
      this.foundLyrics = _.fill(Array(lyrics.length), '');
      this.lyricsLower = _.filter(this.lyricsLower.split(' '), sub => sub.length);
      this.lyricsText = _.filter(this.lyricsText.split(' '), sub => sub.length);
      this.lyrics = _.filter(lyrics.split(' '), sub => sub.length);
      this.stableCopy = _.map(this.lyrics, _.clone);
    },
    getLyrics() {
      this.$http.post('jobs/getlyrics', { artist: 'Elton John', song: 'Tiny Dancer' })
        .then(
          (res) => {
            const body = _.defaults(res.body, {
            });
            this.lyrics = body;
          },
          () => {
            this.$snotify.error('Failed to load data', { timeout: 0 });
          },
        );
    },
    loadLyrics() {
      this.lyrics = "\nBlue jean baby, L.A. lady\nSeamstress for the band\nPretty eyes, pirate smile\nYou'll marry a music man\n\nBallerina, you must have seen her\nDancing in the sand\nAnd now she's in me, always with me\nTiny dancer in my hand\n\nJesus freaks out in the street\nHanding tickets out for God\nTurning back, she just laughs\nThe boulevard is not that bad\n\nPiano man, he makes his stand\nIn the auditorium\nLooking on, she sings the song\nThe words she knows, the tune she hums\n\nBut, oh, how it feels so real\nLying here with no one near\nOnly you, and you can hear me\nWhen I say softly, slowly\n\nHold me closer, tiny dancer\nCount the headlights on the highway\nLay me down in sheets of linen\nYou had a busy day today\n\nHold me closer, tiny dancer\nCount the headlights on the highway\nLay me down in sheets of linen\nYou had a busy day today\n\nBlue jean baby, L.A. lady\nSeamstress for the band\nPretty eyes, pirate smile\nYou'll marry a music man\n\nBallerina, you must have seen her\nDancing in the sand\nAnd now she's in me, always with me\nTiny dancer in my hand\n\nBut, oh, how it feels so real\nLying here with no one near\nOnly you, and you can hear me\nWhen I say softly, slowly\n\nHold me closer, tiny dancer\nCount the headlights on the highway\nLay me down in sheets of linen\nYou had a busy day today\n\nHold me closer, tiny dancer\nCount the headlights on the highway\nLay me down in sheets of linen\nYou had a busy day today\n\n";
    },
  },
};
</script>
