"""GUI 없이 요구사항의 경계 시간과 프레임 데이터를 검증한다."""
from types import SimpleNamespace
import unittest

import animation_viewer as viewer


class PlaybackTests(unittest.TestCase):
    def setUp(self):
        self.animations, self.sizes = viewer.load_animations()
        self.player = viewer.AnimationPlayer(self.animations)

    def test_four_animations_have_different_frame_counts(self):
        self.assertEqual([a.name for a in self.animations],
                         ['Walk', 'Run', 'Jump', 'Attack'])
        self.assertEqual([len(a.frames) for a in self.animations], [8, 8, 6, 6])

    def test_every_frame_is_shown_five_times_before_pause(self):
        for animation in self.animations:
            with self.subTest(animation=animation.name):
                player = viewer.AnimationPlayer((animation,))
                shown = []
                while not player.paused:
                    shown.append(player.frame_index)
                    player.advance(1 / animation.fps)
                self.assertEqual(shown, list(range(len(animation.frames))) * 5)
                self.assertEqual(player.completed_loops, 5)
                self.assertEqual(player.frame_index, len(animation.frames) - 1)

    def test_last_frame_gets_full_duration_before_pause(self):
        self.player.advance(4.875)  # 걷기 8프레임 × 5회 @ 8fps의 마지막 프레임
        self.assertEqual(self.player.frame_index, 7)
        self.assertFalse(self.player.paused)
        self.player.advance(0.124)
        self.assertFalse(self.player.paused)
        self.player.advance(0.001)
        self.assertTrue(self.player.paused)
        self.assertAlmostEqual(self.player.remaining, 1.0)

    def test_pause_holds_last_frame_for_one_second(self):
        self.player.advance(5.0)
        last_frame = self.player.frame
        self.player.advance(0.999)
        self.assertTrue(self.player.paused)
        self.assertIs(self.player.frame, last_frame)
        self.assertEqual(self.player.animation.name, 'Walk')
        self.player.advance(0.001)
        self.assertFalse(self.player.paused)
        self.assertEqual(self.player.animation.name, 'Run')
        self.assertEqual(self.player.frame_index, 0)
        self.assertEqual(self.player.completed_loops, 0)

    def test_animation_order_wraps_for_three_whole_cycles(self):
        expected = ['Walk', 'Run', 'Jump', 'Attack']
        for cycle in range(3):
            for name in expected:
                with self.subTest(cycle=cycle, name=name):
                    self.assertEqual(self.player.animation.name, name)
                    animation = self.player.animation
                    self.player.advance(5 * len(animation.frames) / animation.fps)
                    self.assertTrue(self.player.paused)
                    self.player.advance(1.0)
        self.assertEqual(self.player.animation.name, 'Walk')
        self.assertEqual(self.player.frame_index, 0)

    def test_slow_rendering_does_not_change_playback_speed(self):
        fine = viewer.AnimationPlayer(self.animations)
        coarse = viewer.AnimationPlayer(self.animations)
        for _ in range(1600):
            fine.advance(0.01)
        coarse.advance(16.0)
        self.assertEqual(fine.animation_index, coarse.animation_index)
        self.assertEqual(fine.frame_index, coarse.frame_index)
        self.assertEqual(fine.completed_loops, coarse.completed_loops)
        self.assertEqual(fine.paused, coarse.paused)
        self.assertAlmostEqual(fine.remaining, coarse.remaining)

    def test_time_remainder_survives_pause_boundary(self):
        self.player.advance(6.1)
        self.assertEqual(self.player.animation.name, 'Run')
        self.assertEqual(self.player.frame_index, 1)
        self.assertAlmostEqual(self.player.remaining, 1 / 6 - 0.1)

    def test_invalid_elapsed_time_is_rejected(self):
        for elapsed in (-1, float('nan'), float('inf')):
            with self.subTest(elapsed=elapsed), self.assertRaises(ValueError):
                self.player.advance(elapsed)

    def test_variable_rectangles_remain_inside_both_images_and_canvas(self):
        for animation in self.animations:
            self.assertGreater(len({(f.width, f.height) for f in animation.frames}), 1)
            image_w, image_h = self.sizes[animation.sheet]
            for frame in animation.frames:
                with self.subTest(animation=animation.name, frame=frame):
                    x, bottom, width, height = frame.source_rect(image_h)
                    self.assertGreaterEqual(x, 0)
                    self.assertGreaterEqual(bottom, 0)
                    self.assertLessEqual(x + width, image_w)
                    self.assertLessEqual(bottom + height, image_h)
                    cx, cy, dw, dh = frame.draw_rect(animation.scale)
                    self.assertGreaterEqual(cx - dw / 2, 0)
                    self.assertLessEqual(cx + dw / 2, viewer.CANVAS_WIDTH)
                    self.assertGreaterEqual(cy - dh / 2, 0)
                    self.assertLessEqual(cy + dh / 2, viewer.CANVAS_HEIGHT)
                    self.assertGreaterEqual(dh, viewer.CANVAS_HEIGHT / 2)
                    self.assertAlmostEqual(dw / dh, width / height)

    def test_pico2d_source_coordinates_convert_from_top_to_bottom(self):
        frame = viewer.Frame(10, 20, 30, 40, 25, 40)
        self.assertEqual(frame.source_rect(100), (10, 40, 30, 40))
        self.assertEqual(frame.draw_rect(2), (400, 300, 60, 80))

    def test_escape_and_window_close_work_while_paused(self):
        self.player.advance(5.0)
        self.assertTrue(self.player.paused)
        self.assertTrue(viewer.should_quit([
            SimpleNamespace(type=viewer.pico2d.SDL_QUIT)]))
        self.assertTrue(viewer.should_quit([
            SimpleNamespace(type=viewer.pico2d.SDL_KEYDOWN, key=viewer.pico2d.SDLK_ESCAPE)]))
        self.assertFalse(viewer.should_quit([
            SimpleNamespace(type=viewer.pico2d.SDL_KEYDOWN, key=ord('a'))]))

    def test_wrong_image_dimensions_fail_instead_of_using_wrong_crops(self):
        with self.assertRaises(ValueError):
            viewer.validate_images({'sheet': SimpleNamespace(w=10, h=20)},
                                   {'sheet': [20, 20]})


if __name__ == '__main__':
    unittest.main()
