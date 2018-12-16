/* eslint no-console: 0 */
/* eslint no-undef: 0 */
/* eslint max-len: 0 */

const express = require('express');
const path = require('path');
const fs = require('fs-extra');
const TVDB = require('node-tvdb');
const lyr = require('lyrics-fetcher');
const config = require('../../config');

const routes = express.Router();

routes.post('/getlyrics', async (req, res) => {
  // eslint-disable-next-line
  let song = req.body.song;
  if (song === '' && req.body.artist !== '') {
    const titleFile = path.join(config.directories.storage, `${req.body.artist.toLowerCase()}.txt`);

    if (fs.existsSync(titleFile)) {
      fs.readFile(titleFile, (err, data) => {
        if (err) throw err;
        const songs = data.toString().split('\n');
        song = songs[Math.floor(Math.random() * songs.length)];
        lyr.fetch(req.body.artist, song, (err, lyrics) => {
          res.json({ lyrics: err || lyrics, title: song });
        });
      });
    }
  } else {
    lyr.fetch(req.body.artist, song, (err, lyrics) => {
      res.json({ lyrics: err || lyrics, title: song });
    });
  }
});

module.exports = { routes };
