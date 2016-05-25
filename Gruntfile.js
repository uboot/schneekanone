module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    connect: {
      server: {
        options: {
          port: 9001,
          base: '.',
          livereload: true
        }
      }
    },
    watch: {
      scripts: {
        files: ['Gruntfile.js', '*.html', '*.js'],
        options: {
          spawn: true,
          reload: true,
          livereload: true
        },
      },
    },
  });

  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['connect', 'watch']);

};
