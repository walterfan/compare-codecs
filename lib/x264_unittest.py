#!/usr/bin/python
"""Unit tests for encoder module."""

import unittest
import encoder

import x264

class TestX264(unittest.TestCase):
  def test_Init(self):
    codec = x264.X264Codec()
    self.assertEqual(codec.name, 'x264')

  def test_ScoreResult(self):
    codec = x264.X264Codec()
    result = {'bitrate': 100, 'psnr': 10.0}
    self.assertEqual(10.0, codec.ScoreResult(100, result))
    self.assertEqual(10.0, codec.ScoreResult(1000, result))
    # Score is reduced by 0.1 per kbps overrun.
    self.assertAlmostEqual(10.0 - 0.1, codec.ScoreResult(99, result))
    # Score floors at 0.1 for very large overruns.
    self.assertAlmostEqual(0.1, codec.ScoreResult(1, result))
    self.assertFalse(codec.ScoreResult(100, None))

  def test_OneBlackFrame(self):
    codec = x264.X264Codec()
    videofile = encoder.Videofile(
      'video/testclips/one_black_frame_1024_768_30.yuv')
    encoding = codec.BestEncoding(1000, videofile)
    encoding.Execute()
    score = encoding.Score()
    # Most codecs should be good at this.
    self.assertLess(50.0, encoding.Score())


if __name__ == '__main__':
    unittest.main()


