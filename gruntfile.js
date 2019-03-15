//gruntfile.js
module.exports = function(grunt) {

  grunt.initConfig({
    watch: {

      files: ['**/*.py'],
      tasks: ['shell'], 
      options: {
        cwd: {
          files: 'battdeg/'
        }
      }
    },
    shell: {
      test: {
        command: 'pytest'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-shell');

  grunt.registerTask('default', ['watch']);
  
};

// Add task called 'pylint', different from 'default' to perform pylint on saving
// try this : https://stackoverflow.com/a/52336149/1328232