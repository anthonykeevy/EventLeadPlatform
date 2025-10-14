#!/usr/bin/env node
/**
 * Test runner script for EventLead Platform Frontend
 */
const { execSync } = require('child_process')
const path = require('path')

function runTests() {
  console.log('🧪 Running EventLead Platform Frontend Tests...')
  console.log('=' * 50)
  
  try {
    // Change to frontend directory
    process.chdir(__dirname)
    
    // Run vitest with specific options
    const cmd = [
      'npx vitest',
      'run', // Run tests once instead of watch mode
      '--reporter=verbose', // Verbose output
      '--coverage', // Enable coverage
      '--coverage.reporter=text,html,json', // Coverage reporters
      '--coverage.outputDir=./test-results/coverage', // Coverage output directory
      '--reporter=html', // HTML reporter
      '--outputFile=./test-results/index.html', // HTML output file
    ].join(' ')
    
    execSync(cmd, { stdio: 'inherit' })
    
    console.log('\n✅ All frontend tests passed!')
    return 0
  } catch (error) {
    console.log(`\n❌ Frontend tests failed with exit code ${error.status}`)
    return error.status || 1
  }
}

function runSpecificTests(testPattern) {
  console.log(`🧪 Running frontend tests matching: ${testPattern}`)
  console.log('=' * 50)
  
  try {
    process.chdir(__dirname)
    
    const cmd = [
      'npx vitest',
      'run',
      testPattern,
      '--reporter=verbose',
    ].join(' ')
    
    execSync(cmd, { stdio: 'inherit' })
    
    console.log(`\n✅ Frontend tests matching '${testPattern}' passed!`)
    return 0
  } catch (error) {
    console.log(`\n❌ Frontend tests failed with exit code ${error.status}`)
    return error.status || 1
  }
}

function runAuthTests() {
  return runSpecificTests('**/auth/**/*.test.*')
}

function runUnitTests() {
  console.log('🧪 Running Frontend Unit Tests...')
  console.log('=' * 50)
  
  try {
    process.chdir(__dirname)
    
    const cmd = [
      'npx vitest',
      'run',
      '--reporter=verbose',
      '--coverage',
      '--coverage.reporter=text,html',
    ].join(' ')
    
    execSync(cmd, { stdio: 'inherit' })
    
    console.log('\n✅ All frontend unit tests passed!')
    return 0
  } catch (error) {
    console.log(`\n❌ Frontend unit tests failed with exit code ${error.status}`)
    return error.status || 1
  }
}

function runComponentTests() {
  console.log('🧪 Running Frontend Component Tests...')
  console.log('=' * 50)
  
  try {
    process.chdir(__dirname)
    
    const cmd = [
      'npx vitest',
      'run',
      '**/components/**/*.test.*',
      '**/features/**/*.test.*',
      '--reporter=verbose',
    ].join(' ')
    
    execSync(cmd, { stdio: 'inherit' })
    
    console.log('\n✅ All frontend component tests passed!')
    return 0
  } catch (error) {
    console.log(`\n❌ Frontend component tests failed with exit code ${error.status}`)
    return error.status || 1
  }
}

function showHelp() {
  console.log('Usage: node run-tests.js [command]')
  console.log('Commands:')
  console.log('  (no args) - Run all frontend tests')
  console.log('  auth      - Run authentication tests')
  console.log('  unit      - Run unit tests only')
  console.log('  component - Run component tests only')
  console.log('  help      - Show this help message')
}

// Main execution
const command = process.argv[2]?.toLowerCase()
let exitCode = 0

switch (command) {
  case 'auth':
    exitCode = runAuthTests()
    break
  case 'unit':
    exitCode = runUnitTests()
    break
  case 'component':
    exitCode = runComponentTests()
    break
  case 'help':
    showHelp()
    exitCode = 0
    break
  case undefined:
    exitCode = runTests()
    break
  default:
    console.log(`Unknown command: ${command}`)
    console.log('Use "help" to see available commands')
    exitCode = 1
}

process.exit(exitCode)
