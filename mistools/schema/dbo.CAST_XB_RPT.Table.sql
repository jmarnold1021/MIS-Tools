DROP TABLE [dbo].[CAST_XB_RPT]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_XB_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_XB_RPT](
	[CAST_XB_RPT_ID] [int] NOT NULL,
	[CAST_XB_RPT_FLAG] [bit] NOT NULL,
	[CAST_XB_WORK_ID] [varchar](10) NULL,
	[CASTXB_GI01] [varchar](3) NULL,
	[CASTXB_GI03] [varchar](3) NULL,
	[CASTXB_CB01] [varchar](12) NULL,
	[CASTXB_XB00] [varchar](6) NULL,
	[CASTXB_XB01] [varchar](1) NULL,
	[CASTXB_XB02] [varchar](6) NULL,
	[CASTXB_XB04] [varchar](1) NULL,
	[CASTXB_XB05] [varchar](4) NULL,
	[CASTXB_XB06] [varchar](4) NULL,
	[CASTXB_XB08] [varchar](1) NULL,
	[CASTXB_XB09] [varchar](1) NULL,
	[CASTXB_XB10] [varchar](1) NULL,
	[CASTXB_UNIQUE_IDX] [varchar](23) NULL,
	[CASTXB_SEC_NAME_IDX] [varchar](19) NULL,
	[CASTXB_COURSE_SECTIONS_ID] [varchar](19) NULL,
	[CASTXB_XB11] [varchar](6) NULL,
	[CASTXB_CB00] [varchar](12) NULL,
	[CASTXB_XB12] [varchar](1) NULL,
 CONSTRAINT [PK_XB_RPT_ID] PRIMARY KEY CLUSTERED 
(
	[CAST_XB_RPT_ID] DESC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
