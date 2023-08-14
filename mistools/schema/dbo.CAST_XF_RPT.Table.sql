DROP TABLE [dbo].[CAST_XF_RPT]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_XF_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_XF_RPT](
	[CAST_XF_RPT_ID] [int] NOT NULL,
	[CAST_XF_RPT_FLAG] [bit] NOT NULL,
	[CAST_XF_WORK_ID] [varchar](10) NULL,
	[CASTXF_GI01] [varchar](3) NULL,
	[CASTXF_GI03] [varchar](3) NULL,
	[CASTXF_CB01] [varchar](12) NULL,
	[CASTXF_XB00] [varchar](6) NULL,
	[CASTXF_XF00] [varchar](2) NULL,
	[CASTXF_XF01] [varchar](2) NULL,
	[CASTXF_XF02] [varchar](6) NULL,
	[CASTXF_XF03] [varchar](6) NULL,
	[CASTXF_XF04] [varchar](9) NULL,
	[CASTXF_XF05] [varchar](8) NULL,
	[CASTXF_XF06] [varchar](8) NULL,
	[CASTXF_XF07] [varchar](5) NULL,
	[CASTXF_COURSE_SEC_MEETING_ID] [varchar](10) NULL,
	[CASTXF_COURSE_SECTIONS_ID] [varchar](19) NULL,
	[CASTXF_UNIQUE_IDX] [varchar](34) NULL,
	[CASTXF_CB00] [varchar](12) NULL,
 CONSTRAINT [PK_XF_RPT_ID] PRIMARY KEY CLUSTERED 
(
	[CAST_XF_RPT_ID] DESC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__CAST_XF_R__CAST___1D060F5C]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[CAST_XF_RPT] ADD  DEFAULT ((1)) FOR [CAST_XF_RPT_FLAG]
END
GO